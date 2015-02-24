#include "serial_handling.h"

#include <Arduino.h>
#include <errno.h>
#include <assert13.h>
#include <stdio.h> // isdigit

// replace the next two functions with your implementation
// of the communication with the server
int srv_get_pathlen(LonLat32 start, LonLat32 end) {
    send_coords(&start, &end);
    uint16_t count_len = 100;
    char *msg = (char *)malloc(sizeof(*msg) * count_len);
    if (msg == NULL)
        return -1;

    uint16_t nread = serial_readline(msg, count_len);

#ifndef DEBUG
    comment_debug_ln("MSG: ");
    comment_debug_ln(msg);
#endif // DEBUG

    int32_t v = 0;
    
    while (parse_first_digits(msg, count_len, &v) < 0);

    comment_debug_ln("FLUX ");
    comment_debug_ln(v, DEC);

    free(msg);

    return v;
}

bool int10Part(const char c) {
    return c == '-' || c == '+' || isdigit(c);
}

// Greedy parse till the first encounter of digits and then
// returns the end index on which the last digit was found
int16_t parse_first_digits(const char *str, const uint16_t len, int32_t *sav) {
    if (str == NULL || len < 1)
        return -1;

    int16_t start, end;
    start = end = 0;
    const char *t = str;
    while (!int10Part(*t) && start < len) {
        ++t;
        ++start;
    }

    if (*t == '\0' || start >= len)
        return -1;

    end = start;
    while (int10Part(*t) && end < len) {
        ++t;
        ++end;
    }
    if (end >= len)
        return -1;

    char *endPtr = (char *)malloc(sizeof(*endPtr) * (len - end));
    *sav = strtol(str + start, &endPtr, 10);
    free(endPtr);

    return  end;
}

LonLat32 get_waypoint() {
    int32_t lat, lon;
    uint16_t index, nchars = 40;
    char *line = (char *)malloc(sizeof(*line) * nchars);

    if (line == NULL) {
        comment_debug_ln("No Memory! ");
        comment_debug_ln(__LINE__);
        comment_debug_ln(__FILE__" ");
        return NULL;
    }

    int nread = serial_readline(line, nchars);
    comment_debug_ln("nread ");
    comment_debug_ln(nread);
    // TODO: Check for nread
    index = parse_first_digits(line, nchars, &lat);
    
    index = parse_first_digits(line + index, nchars - index, &lon);

    // Clean up
    free(line);
    return LonLat32(lat, lon);
}

void debug_waypoint(const LonLat32 pt) {
    comment_debug_ln(pt.lon);
    comment_debug_ln(pt.lat);
}

uint16_t serial_readline(char *line, uint16_t line_size) {
    int bytes_read = 0;    // Number of bytes read from the serial port.

    // Read until we hit the maximum length, or a newline.
    // One less than the maximum length because we want to add a null terminator.
    Serial.setTimeout(1000);
    while (bytes_read < line_size - 1) {
        while (Serial.available() == 0) {
            // There is no data to be read from the serial port.
            // Wait until data is available.
            return 0;
        }

        line[bytes_read] = (char) Serial.read();

        // A newline is given by \r or \n, or some combination of both
        // or the read may have failed and returned 0
        if ( line[bytes_read] == '\r' || line[bytes_read] == '\n' ||
             line[bytes_read] == 0 ) {
                // We ran into a newline character!  Overwrite it with \0
                break;    // Break out of this - we are done reading a line.
        } else {
            bytes_read++;
        }
    }

    // Add null termination to the end of our string.
    line[bytes_read] = '\0';

#ifdef DEBUG
    comment_debug_ln(line);
#endif // DEBUG

    return bytes_read;
}

uint16_t string_read_field(const char *str, uint16_t str_start
    , char *field, uint16_t field_size, const char *sep) {

    // Want to read from the string until we encounter the separator.

    // Character that we are reading from the string.
    uint16_t str_index = str_start;    

    while (1) {
        if ( str[str_index] == '\0') {
            str_index++;  // signal off end of str
            break;
        }

        if ( field_size <= 1 ) break;

        if (strchr(sep, str[str_index])) {
            // field finished, skip over the separator character.
            str_index++;    
            break;
        }

        // Copy the string character into buffer and move over to next
        *field = str[str_index];    
        field++;
        field_size--;
        // Move on to the next character.
        str_index++;    
    }

    // Make sure to add NULL termination to our new string.
    *field = '\0';

    // Return the index of where the next token begins.
    return str_index;    
}

int32_t string_get_int(const char *str) {
    // Attempt to convert the string to an integer using strtol...
    int32_t val = strtol(str, NULL, 10);

    if (val == 0) {
        // Must check errno for possible error.
        if (errno == ERANGE) {
            Serial.print("string_get_int failed: "); Serial.println(str);
            assert13(0, errno);
        }
    }

    return val;
}

void send_ack() {
    Serial.println("A");
    Serial.flush();
}

void parse_ack() {
    int count_len = 4;
    char msg[count_len];
    while (serial_readline(msg, count_len) < 1 || msg[0] != 'A');
}

void send_eos() {
    Serial.println("E");
    Serial.flush();
}

void parse_eos() {
    int count_len = 4;
    char msg[count_len];
    uint16_t nread = serial_readline(msg, count_len);
}

void send_coords(const LonLat32 *start, const LonLat32 *end) {
    Serial.print("R ");
    Serial.print(start->lat);
    Serial.print(" ");
    Serial.print(start->lon);
    Serial.print(" ");
    Serial.print(end->lat);
    Serial.print(" ");
    Serial.print(end->lon);
    Serial.println();
    Serial.flush();
}
