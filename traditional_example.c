#include <stdio.h>
#include <math.h>

// Traditional computation similar to quantum operations
double quantum_like_operation(double state1, double state2, double phase) {
    double result = 0.0;
    
    // Hadamard-like transformation
    double h_state1 = (state1 + state2) / sqrt(2.0);
    double h_state2 = (state1 - state2) / sqrt(2.0);
    
    // Phase rotation
    double rotated = h_state1 * cos(phase) - h_state2 * sin(phase);
    
    // Measurement simulation
    result = rotated * rotated;
    
    return result;
}

int main() {
    double result = quantum_like_operation(1.0, 0.0, 3.14159/4);
    printf("Result: %f\n", result);
    return 0;
}
