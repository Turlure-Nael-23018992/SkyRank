#include <iostream>
#include <vector>

extern "C" {

void lm(bool* dom, int* sky, int* skyCard, int n, int i, int j, int prof) {
    for (int k = 0; k < n; ++k) {
        if (dom[k * n + j]) {
            if (sky[i * n + k] > 0 && skyCard[i] > 0) {
                dom[k * n + j] = false;
                int value = sky[i * n + k];
                if (value == 1 || value > prof) {
                    sky[i * n + k] = prof;
                }
                skyCard[i] -= 1;
            }
            if (skyCard[i] == 0) {
                return;
            }
            int new_prof = prof + 1;
            lm(dom, sky, skyCard, n, i, k, new_prof);
        }
    }
}

void calculLm(bool* dom, int* sky, int* skyCard, int n) {
    for (int k = 0; k < n; ++k) {
        lm(dom, sky, skyCard, n, k, k, 2);
    }
}
}
