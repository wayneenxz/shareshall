import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

### **Step 1: Load Extracted Entity Data** ###
wikileaks_entities_df = pd.read_excel("wikileaks_entities.xlsx")
news_entities_df = pd.read_excel("news_entities.xlsx")

### **Step 2: Extract Relationships Between Entities (Optimized)** ###
def extract_relationships(df, source_col):
    relationships = []
    
    for _, row in df.iterrows():
        try:
            entities = eval(row["Extracted Entities"])  # Convert string to list of tuples
            entity_names = [ent[0] for ent in entities]
            
            # Limit relationships to highly connected entities
            if len(entity_names) > 1:
                for i in range(len(entity_names)):
                    for j in range(i + 1, len(entity_names)):
                        relationships.append((entity_names[i], entity_names[j], row[source_col]))
        except:
            continue  # Ignore rows with errors

    return relationships

# Extract relationships from both datasets
wikileaks_relationships = extract_relationships(wikileaks_entities_df, "PDF Path")
news_relationships = extract_relationships(news_entities_df, "Link")

# Combine all relationships
all_relationships = wikileaks_relationships + news_relationships

# **Optimization: Only keep the most frequently connected entities**
top_entities = Counter([pair[0] for pair in all_relationships] + [pair[1] for pair in all_relationships])
important_entities = {node for node, count in top_entities.items() if count > 2}  # Keep nodes with >2 connections

# Filter relationships to keep only important entities
filtered_relationships = [(e1, e2, src) for e1, e2, src in all_relationships if e1 in important_entities and e2 in important_entities]

# Save relationships (optional debugging)
relationships_df = pd.DataFrame(filtered_relationships, columns=["Entity1", "Entity2", "Source"])
relationships_df.to_excel("entity_relationships_filtered.xlsx", index=False)
print("✅ Filtered relationships saved as 'entity_relationships_filtered.xlsx'.")

### **Step 3: Build & Visualize the Optimized Graph** ###
# Create Graph
G = nx.Graph()

# Add edges (relationships between important entities)
for entity1, entity2, source in filtered_relationships:
    G.add_edge(entity1, entity2, label=source)

# **Optimization: Faster Layout & Simplified Graph**
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.7, seed=42)  # Faster layout with better separation

# **Color by Entity Type**
node_colors = ["lightblue" if "Inc." in node or "Company" in node else "lightgreen" for node in G.nodes()]

# **Draw Graph (Optimized)**
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=1500, font_size=8, font_weight="bold")

plt.title("Optimized Entity Relationship Graph")
plt.show()
