#ifndef UTILS_H
#define UTILS_H
/**
 * @brief compares the two null-terminated sameStrings
 *
 * @param s1 first string
 * @param s2 second string
 *
 * @return s1 == s2 ? 1 : 0
 */
int sameStrings(char*, char*);


/**
 * @brief splits a string into substrings ended by seperator or null terminator.
 *
 * @param array pointer to a variable of 2D array to store the sameStrings
 * @param str string waiting to be splitted
 * @param seperator the seperating
 *
 * @return Amount of substrings, i.e. size of array.
 *
 * @usage
 * int lines = split(&arr, "Hello World and me!", ' ');
 * // arr[0] == "Hello"
 * // arr[1] == "World!"
 * // arr[2] == "and"
 * // arr[3] == "me!"
 */
int split(char***, char*, char);

#endif
