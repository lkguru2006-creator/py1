#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

// Simple buffer to hold response (for non-streaming, but we want streaming)
// For streaming, we just print directly in the callback.

size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total_size = size * nmemb;
    // Print directly to stdout to achieve streaming effect
    fwrite(ptr, size, nmemb, stdout);
    fflush(stdout); // Ensure it appears immediately
    return total_size;
}

int main(void) {
    CURL *curl;
    CURLcode res;
    char input[1024];

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if (!curl) {
        fprintf(stderr, "Error initializing curl.\n");
        return 1;
    }

    printf("=======================================\n");
    printf("      MetaChat Native Client (C)       \n");
    printf("=======================================\n");
    printf("Type 'exit' to quit.\n\n");

    while (1) {
        printf("\nYou > ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        
        // Remove newline
        input[strcspn(input, "\n")] = 0;

        if (strcmp(input, "exit") == 0) break;

        // JSON payload: {"message": "input"}
        // Simple manual JSON construction (BE CAREFUL with quotes in real apps)
        char json_payload[2048];
        snprintf(json_payload, sizeof(json_payload), "{\"message\": \"%s\"}", input);

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000/chat");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_payload);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        
        printf("Meta AI > ");
        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            fprintf(stderr, "\nRequest failed: %s\n", curl_easy_strerror(res));
        }
        
        printf("\n"); // New line after response
        curl_slist_free_all(headers);
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    printf("Goodbye!\n");
    return 0;
}
