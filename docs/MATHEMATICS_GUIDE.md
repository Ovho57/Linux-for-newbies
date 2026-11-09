# Mathematics behind a neural network

## Weighted sum
A neuron combines inputs using weights and a bias:
z = w1*x1 + w2*x2 + ... + wn*xn + b

For x1=2, w1=0.5, x2=3, w2=0.8 and b=0.2:
z = (0.5*2) + (0.8*3) + 0.2 = 3.6

## Activation
The initial engine applies tanh to hidden layers and sigmoid to the output.
sigmoid(z) = 1 / (1 + exp(-z))

## Matrix form
For a batch:
Z = XW + b
A = activation(Z)

## Mean squared error
MSE = mean((prediction - target)^2)
Lower training loss means predictions are closer to training targets under this measure. It does not prove good performance on unseen data.

## Gradient descent
W = W - learning_rate * gradient
The learning rate controls update size.

## Backpropagation
Backpropagation uses the chain rule to calculate how parameters affect loss. Gradients are propagated from output toward earlier layers and parameters are updated.
