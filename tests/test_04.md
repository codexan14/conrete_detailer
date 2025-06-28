# Test 04

## Problem
Let a column $400 \times 600 \text{ mm}^2 $ with $ 4\, \phi 25\, \text{mm}$ in the corner, 2 $\phi 19\, \text{mm}$ between corner bars. 

1. Determine the maximum force that the column can bear.
2. Determine the flexural moment that the column can bear along the x-axis.
3. Determine the flexural moment that the column can bear along the y-axis.

## Sign Convention
- Tension stress is positive 
- Compression stress is negative
- Clockwise moment is positive
- Counterclockwise moment is negative

## Solution

### 1. Maximum Force
The maximum force is: 

$$ 
    \begin{align} 
        F   &= C_c + \sum A_{si} f_{si} \nonumber \\
            &= 0.85 f'c A_c + \sum A_{si} f_{y} \nonumber \\
            &= 0.85 (28 \text{ MPa}) (400 \times 600 \text{ mm}^2) + (4231.72530\, \text{mm}^2)(420\, \text{MPa}) \nonumber \\
            &= 5712000.0 \text{ N} + 1777324.6278 \text{ N} \nonumber \\ 
            &= 7489324.6278 \text{ N} \nonumber
 \end{align}
 $$

### 2. Flexural Moment Along X-Axis
The equation of equilibrium must hold: 
$$
    \begin{align}
        0   &= C_c + \sum A_{si} f_{si} \nonumber \\ 
            & = 0.85 f'_c a b + \sum A_{si} f_{si} \nonumber \\
            & = 0.85 f'_c \beta_1 c b + \sum A_{si}  \text{clamp} \left(E \varepsilon_i, -f_y, f_y \right) \nonumber \\
            & = 0.85 f'_c \beta_1 c b + E \sum A_{si}  \text{clamp} \left(\varepsilon_i, -\varepsilon_y, \varepsilon_y \right) \nonumber \\
            & = 0.85 f'_c \beta_1 c b + E \sum A_{si}  \text{clamp} \left(\theta(y_i-c), -\varepsilon_y, \varepsilon_y \right) \nonumber \\
            & = 0.85 f'_c \beta_1 c b + E \sum A_{si}  \text{clamp} \left(\frac{0.003}{c}(y_i-c), -\varepsilon_y, \varepsilon_y \right) \nonumber
    \end{align}
$$

The first approximation will be assuming no yielding behaviour: 

$$
    \begin{align}
        0 & = 0.85 f'_c \beta_1 c b + E  \frac{0.003}{c} \sum A_{si}(y_i-c) \nonumber  \\
        & = 0.85 f'_c \beta_1 c b + E  \frac{0.003}{c} \left(\sum A_{si}(y_i) - \sum A_{si}(c) \right) \nonumber  \\
    \end{align}
$$