from torch import nn
import torch


class NeuralNetwork(nn.Module):
    """
        Brain for the simulation entities

        input = [neighbour_wolf_number, neighbour_sheep_number, old_direction_x, old_direction_y]
        output = [new_direction_x, new_direction_y]
    """
    def __init__(self, input_size = 4, hidden_size=64, output_size=2, params=None):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
        
        if params:
            self.load_params(params)

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
    
    def load_params(self, params):
        self.load_state_dict(params)

    def get_params(self):
        return self.state_dict()
    
    def save(self, path):
        torch.save(self.state_dict(), path)