import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, random_split, DataLoader

torch.manual_seed(42)
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fx1 = nn.Linear(20,25)
        self.attn = nn.Linear(25,25)
        self.fx2 = nn.Linear(25,1)
        self.drop = nn.Dropout(0.5)
    
    def forward(self,x):
        x = torch.relu(self.fx1(x))
        query = self.attn(x)
        key = value = x
        attn_scores = torch.matmul(query, key.transpose(1,0))
        attn_weights = torch.softmax(attn_scores, dim=-1)
        context_vector = torch.matmul(attn_weights, value)
        x = self.fx2(context_vector)
        return x

class TransformerChatbot(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads):
        super().__init__()
        # 1. Learnable Word Embeddings (replaces TF-IDF)
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        
        # 2. Positional Encoding (Transformers need to know word order)
        self.pos_encoding = nn.Parameter(torch.randn(1, 100, embed_dim)) 

        # 3. Multi-Head Attention (Evolution of your attn layer)
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        
        self.fc = nn.Linear(embed_dim, vocab_size) # Predicts the next word

    def forward(self, x):
        # x shape: [batch_size, seq_len]
        x = self.embedding(x) + self.pos_encoding[:, :x.size(1), :]
        
        # MultiheadAttention expects [seq_len, batch_size, embed_dim]
        x = x.transpose(0, 1)
        attn_output, _ = self.attention(x, x, x) # Self-Attention
        
        x = self.fc(attn_output.transpose(0, 1))
        return x

X = torch.randn(1000,20)
# Create a mathematical relationship: 
# If the sum of features is positive, label is 1, otherwise 0.
y = (X.sum(dim=1, keepdim=True) > 0).float()
dataset = TensorDataset(X,y)
n_train = int(0.8*len(X))
n_test = len(X) - n_train
train_dataset, test_dataset = random_split(dataset, [n_train, n_test])
train = DataLoader(train_dataset, batch_size = 100, shuffle = True)
test = DataLoader(test_dataset, batch_size=100)

model = SimpleNN()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr = 0.01)

epochs = 50
for epoch in range(epochs):
    model.train()
    for inputs, targets in train:
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if (epoch+1)%10 == 0:
            print(f'Epoch:{epoch+1}/{epochs}, Loss:{loss.item()}')
            with torch.no_grad():
                model.eval()
                for inputs, targets in test:
                    predictions = model(inputs)
                    predictions = (predictions>0.5).float()
                    accuracy = (predictions == targets).sum()/targets.size(0)
                    print(f'Accuracy:{accuracy:.6f}')

# --- ML TESTING SUITE ---
model.eval()
print("\n--- Running Product Validation Tests ---")

with torch.no_grad():
    # 1. Edge Case: The "Zero" Vector (Should be 0)
    zero_input = torch.zeros(1, 20)
    zero_pred = torch.sigmoid(model(zero_input)).item()
    print(f"Test 1 [Zero Input]: {'PASS' if zero_pred < 0.5 else 'FAIL'} (Score: {zero_pred:.4f})")

    # 2. Extreme Case: Large Positive/Negative Values
    pos_input = torch.ones(1, 20) * 100
    neg_input = torch.ones(1, 20) * -100
    pos_pred = torch.sigmoid(model(pos_input)).item()
    neg_pred = torch.sigmoid(model(neg_input)).item()
    print(f"Test 2 [Extreme Positive]: {'PASS' if pos_pred > 0.99 else 'FAIL'} (Score: {pos_pred:.4f})")
    print(f"Test 3 [Extreme Negative]: {'PASS' if neg_pred < 0.01 else 'FAIL'} (Score: {neg_pred:.4f})")

    # 3. Robustness: Close to the Decision Boundary
    # Sum is barely positive (0.01)
    boundary_input = torch.zeros(1, 20)
    boundary_input[0, 0] = 0.01 
    boundary_pred = torch.sigmoid(model(boundary_input)).item()
    print(f"Test 4 [Boundary Check]: {'PASS' if boundary_pred > 0.5 else 'FAIL'} (Score: {boundary_pred:.4f})")
