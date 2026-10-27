from collections import deque
import numpy as np
import random
from tensorflow.keras.layers import Dense, Flatten, Conv2D, InputLayer, Concatenate, Input
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model

class DQNAgent:
    def __init__(self, state_shape, n_actions, epsilon=0.8, gamma=0.90, cache_weights_name="last_weights",replay_buffer_size=5000):
        self.state_shape = state_shape
        self.n_actions = n_actions
        self.epsilon = epsilon
        self.gamma = gamma
        self.replay_buffer = deque(maxlen=replay_buffer_size)
        self.cache_weights_name =  cache_weights_name
        
        self._reget()

    def _build_model(self):
        model = Sequential()
        model.add(Input(shape=self.state_shape))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.n_actions, activation='linear'))

        model.compile(optimizer='adam', loss='mse')
        return model


        
    def summary(self):
        return self.main_nn.summary()

    def plot_model(self,dpi):
        return plot_model(self.main_nn, to_file='model.png', show_shapes=True, show_layer_names=True, dpi = dpi)
        
    def _reget(self):
        try:
            m = load_model(f"{self.cache_weights_name}.keras")
            self.main_nn = self._build_model()
            self.target_nn = self._build_model()
            
            self.main_nn.set_weights(m.get_weights())
            self.target_nn.set_weights(self.main_nn.get_weights())
            print("Weights loaded")
        except:
            print("No weights found, init random weights")
            self.main_nn = self._build_model()
            self.target_nn = self._build_model()
            self.target_nn.set_weights(self.main_nn.get_weights())

    def save_nn(self, name=None):
        if name != None:
            self.main_nn.save(f"{name}.keras")
        else:
            self.main_nn.save(f"{self.cache_weights_name}.keras")

    def store_transiton(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def epsilon_greedy_policy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            predictions = self.main_nn.predict(state,verbose=0)  # ex: [[0.1, 0.2, 0.3, 0.4]]
            return np.argmax(predictions[0])

    def train(self, mini_batch):
        samples = random.sample(self.replay_buffer, mini_batch)

        for state, action, reward, next_state, done in samples:
            if done:
                target = reward
            else:
                a = np.argmax(self.main_nn.predict(next_state,verbose=0)[0])
                target = reward + self.gamma * self.target_nn.predict(next_state,verbose=0)[0][a]

            Q_values = self.main_nn.predict(state,verbose=0)
            Q_values[0][action] = target

            self.main_nn.fit(state, Q_values, epochs=1, verbose=0)

    def act(self, state):
        predictions = self.main_nn.predict(state,verbose=0)  # ex: [[0.1, 0.2, 0.3, 0.4]]
        return np.argmax(predictions[0])
        
    def update_epsilon(self):
        self.epsilon =  max(0.1, 0.9995 * self.epsilon)

    def update_target_network_soft(self):
        TAU = 1e-3
        for target_weights, q_net_weights in zip(self.target_nn.weights, self.main_nn.weights):
            target_weights.assign(TAU * q_net_weights + (1.0 - TAU) * target_weights)
    
    def update_target_network_hard(self):
        self.target_nn.set_weights(self.main_nn.get_weights())

    def get_epsilion(self):
        return self.epsilon
        
    def set_epsilion(self, epsilon):
        self.epsilon = epsilon