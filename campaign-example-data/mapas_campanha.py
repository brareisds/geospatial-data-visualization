import csv
import geobr
import matplotlib.pyplot as plt
import geobr
import os

# Load data
def load_locations():
    campaigns = {}
    with open('campanhas_exemplo.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip header
        for line in csv_reader:
            name, startDate, endDate, description, state = line
            if name not in campaigns:
                campaigns[name] = []  # Initialize list for each campaign
            campaigns[name].append(state)  # Add state to the campaign's list
    return campaigns

def process_groups(campaigns):
    results = []
    for name, states in campaigns.items():
        print("name:", name)
        print("states:", states)
        results.append((name, states))
    return results

def generate_map(campaigns):
    states = geobr.read_state(year=2020)
    colors = plt.cm.tab20.colors  # Cores diferentes para cada campanha

    j = 1
    for i, (name, states_list) in enumerate(campaigns):
        fig, ax = plt.subplots(figsize=(10, 10))
        states.plot(facecolor="lightgrey", edgecolor="white", ax=ax, linewidth=0.3)

        for state_name in states_list:
            if state_name in states["name_state"].values:
                state = states[states["name_state"] == state_name]
                state.plot(ax=ax, color=colors[i])

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Mapa da {name}")
        #plt.show()
        # plt.savefig(os.path.join(directory, f"Figure_{i}.png"))
        plt.savefig(os.path.join(f'Campanha{j}.png'), dpi=150)
        j += 1


campaigns = load_locations()  # Call the function to load locations
results = process_groups(campaigns)  # Process the loaded campaigns
print(results)
# Usar a função para gerar os mapas
generate_map(results)
