import networkx as nx
import matplotlib.pyplot as plt
from Model.GraphAction import StateLevel as PropositionLevel, ActionLevel, PersistenceAction
from Model.Predicate import Predicate

class GraphPlot:
    """Visualizes planning graph using NetworkX and Matplotlib."""
    def __init__(self):
        pass

    def print_level(self, level_index, levels):
        """Print proposition or action level details."""
        level = levels[level_index]
        if isinstance(level, PropositionLevel):
            prop_level_num = level_index // 2
            print(f"Proposition Level {prop_level_num}:")
            pos_formatted = [f"{p.name}(" + ",".join([ent.name for ent in p.entities]) + ")" for p in sorted(level.positive_literals, key=str)]
            neg_formatted = [f"~{p.name}(" + ",".join([ent.name for ent in p.entities]) + ")" for p in sorted(level.negative_literals, key=str)]
            print("Propositions:", sorted(pos_formatted + neg_formatted))
            mutexes_formatted = []
            for m in level.literal_mutex:
                pair = list(m)
                if len(pair) == 2:
                    (p1, v1), (p2, v2) = pair
                    p1_str = f"~{p1}" if not v1 else str(p1)
                    p2_str = f"~{p2}" if not v2 else str(p2)
                    mutexes_formatted.append((p1_str, p2_str))
            print("Literal Mutexes:", sorted(mutexes_formatted, key=str))
        elif isinstance(level, ActionLevel):
            action_level_num = (level_index - 1) // 2
            print(f"Action Level {action_level_num}:")
            print("Actions:", [str(a) if not isinstance(a, PersistenceAction) else (f"Persist({a.proposition})" if a.is_positive else f"Persist(~{a.proposition})") 
                             for a in sorted(level.actions, key=str)])
            print("Action Mutexes:", [tuple(str(a) for a in m) for m in sorted(level.action_mutex, key=str)])

    def plot_graph(self, levels):
        """Visualize planning graph with NetworkX and Matplotlib."""
        G = nx.DiGraph()
        pos = {}
        labels = {}
        node_shapes = {}

        for i, level in enumerate(levels):
            x = i * 1.5
            if isinstance(level, PropositionLevel):
                level_num = i // 2
                level_label = f"S{level_num}"
                G.add_node(level_label)
                pos[level_label] = (x, 0)
                labels[level_label] = level_label
                node_shapes[level_label] = "o"
                # Add nodes for propositions
                # Create separate nodes for positive and negative literals
                sorted_pos = sorted(level.positive_literals, key=str)
                sorted_neg = sorted(level.negative_literals, key=str)
                all_literals = [(p, True) for p in sorted_pos] + [(p, False) for p in sorted_neg]
                
                for idx, (prop, is_positive) in enumerate(all_literals):
                    if is_positive:
                        prop_node = f"{level_label}_{str(prop)}"
                        label_text = f"{prop.name}(" + ",".join([ent.name for ent in prop.entities]) + ")"
                    else:
                        prop_node = f"{level_label}_~{str(prop)}"
                        label_text = "¬" + f"{prop.name}(" + ",".join([ent.name for ent in prop.entities]) + ")"
                    G.add_node(prop_node)
                    pos[prop_node] = (x, -len(all_literals) + idx)
                    labels[prop_node] = label_text
                    node_shapes[prop_node] = "o"
            else:
                level_num = (i - 1) // 2
                level_label = f"A{level_num}"
                # Add action level node
                G.add_node(level_label)
                pos[level_label] = (x, 0)
                labels[level_label] = level_label
                node_shapes[level_label] = "o"
                # Separate regular and persistence actions
                regular_actions = [a for a in level.actions if not isinstance(a, PersistenceAction)]
                persistence_actions = [a for a in level.actions if isinstance(a, PersistenceAction)]
                # Add nodes for regular actions
                for action in regular_actions:
                    action_node = f"{level_label}_{action.name}"
                    G.add_node(action_node)
                    pos[action_node] = (x, -len(level.actions) + regular_actions.index(action))
                    labels[action_node] = action.name
                    node_shapes[action_node] = "o"
                # Add nodes for persistence actions
                for action in persistence_actions:
                    if action.is_positive:
                        action_node = f"{level_label}_Persist_{str(action.proposition)}"
                    else:
                        action_node = f"{level_label}_Persist_~{str(action.proposition)}"
                    G.add_node(action_node)
                    pos[action_node] = (x, -len(level.actions) + len(regular_actions) + persistence_actions.index(action))
                    if action.is_positive:
                        labels[action_node] = f"Persist({action.proposition})"
                    else:
                        labels[action_node] = f"Persist(¬{action.proposition})"
                    node_shapes[action_node] = "s"

        # Add edges for preconditions and effects
        for i in range(len(levels) - 1):
            if isinstance(levels[i], PropositionLevel) and isinstance(levels[i + 1], ActionLevel):
                prop_level = levels[i]
                action_level = levels[i + 1]
                prop_label = f"S{i//2}"
                act_label = f"A{(i+1-1)//2}"
                # Add edges from preconditions to actions
                for action in action_level.actions:
                    if isinstance(action, PersistenceAction):
                        if action.is_positive:
                            action_node = f"{act_label}_Persist_{str(action.proposition)}"
                        else:
                            action_node = f"{act_label}_Persist_~{str(action.proposition)}"
                        for precond in action.positive_preconditions:
                            if precond in prop_level.positive_literals:
                                precond_node = f"{prop_label}_{str(precond)}"
                                G.add_edge(precond_node, action_node, style="solid")
                        for precond in action.negative_preconditions:
                            if precond in prop_level.negative_literals:
                                precond_node = f"{prop_label}_~{str(precond)}"
                                G.add_edge(precond_node, action_node, style="dashed")
                    else:
                        action_node = f"{act_label}_{action.name}"
                        for precond in action.positive_preconditions:
                            if precond in prop_level.positive_literals:
                                precond_node = f"{prop_label}_{str(precond)}"
                                G.add_edge(precond_node, action_node, style="solid")
                        for neg_precond in action.negative_preconditions:
                            if neg_precond in prop_level.negative_literals:
                                precond_node = f"{prop_label}_~{str(neg_precond)}"
                                G.add_edge(precond_node, action_node, style="dashed")
            elif isinstance(levels[i], ActionLevel) and isinstance(levels[i + 1], PropositionLevel):
                action_level = levels[i]
                prop_level = levels[i + 1]
                act_label = f"A{(i-1)//2}"
                prop_label = f"S{(i+1)//2}"
                # Add edges from actions to effects
                for action in action_level.actions:
                    if isinstance(action, PersistenceAction):
                        if action.is_positive:
                            action_node = f"{act_label}_Persist_{str(action.proposition)}"
                        else:
                            action_node = f"{act_label}_Persist_~{str(action.proposition)}"
                        for effect in action.add_list:
                            if effect in prop_level.positive_literals:
                                effect_node = f"{prop_label}_{str(effect)}"
                                G.add_edge(action_node, effect_node, style="solid")
                        for del_effect in action.delete_list:
                            if del_effect in prop_level.negative_literals:
                                effect_node = f"{prop_label}_~{str(del_effect)}"
                                G.add_edge(action_node, effect_node, style="dashed")
                    else:
                        action_node = f"{act_label}_{action.name}"
                        for effect in action.add_list:
                            if effect in prop_level.positive_literals:
                                effect_node = f"{prop_label}_{str(effect)}"
                                G.add_edge(action_node, effect_node, style="solid")
                        for del_effect in action.delete_list:
                            if del_effect in prop_level.negative_literals:
                                effect_node = f"{prop_label}_~{str(del_effect)}"
                                G.add_edge(action_node, effect_node, style="dashed")

        # Add mutex edges
        for i, level in enumerate(levels):
            level_label = f"S{i//2}" if isinstance(level, PropositionLevel) else f"A{(i-1)//2}"
            if isinstance(level, ActionLevel):
                # Add mutex edges between actions
                for mutex_pair in level.action_mutex:
                    a1, a2 = mutex_pair
                    if not isinstance(a1, PersistenceAction):
                        node1 = f"{level_label}_{a1.name}"
                    else:
                        node1 = f"{level_label}_Persist_{str(a1.proposition)}" if a1.is_positive else f"{level_label}_Persist_~{str(a1.proposition)}"
                    if not isinstance(a2, PersistenceAction):
                        node2 = f"{level_label}_{a2.name}"
                    else:
                        node2 = f"{level_label}_Persist_{str(a2.proposition)}" if a2.is_positive else f"{level_label}_Persist_~{str(a2.proposition)}"
                    if node1 in G.nodes() and node2 in G.nodes() and node1 != node2:
                        G.add_edge(node1, node2, style="curved", color="red")
            elif isinstance(level, PropositionLevel):
                # Add mutex edges between propositions
                # literal_mutex stores frozensets of ((Predicate, bool), (Predicate, bool))
                for mutex_pair in level.literal_mutex:
                    pair = list(mutex_pair)
                    if len(pair) == 2:
                        (p1, v1), (p2, v2) = pair
                        # Node names include ~ prefix for negative literals
                        if v1:
                            node1 = f"{level_label}_{str(p1)}"
                        else:
                            node1 = f"{level_label}_~{str(p1)}"
                        if v2:
                            node2 = f"{level_label}_{str(p2)}"
                        else:
                            node2 = f"{level_label}_~{str(p2)}"
                        if node1 in G.nodes() and node2 in G.nodes() and node1 != node2:
                            G.add_edge(node1, node2, style="curved", color="red")

        # Draw the graph
        node_colors = []
        for node in G.nodes():
            if node.startswith("S"):
                node_colors.append("lightblue")
            elif node.startswith("A"):
                if "Persist" in node:
                    node_colors.append("white")
                else:
                    node_colors.append("lightgreen")

        plt.figure(figsize=(15, 10))
        for node in G.nodes():
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=node_colors[list(G.nodes()).index(node)], 
                                 node_shape=node_shapes[node], node_size=1000)
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if d["style"] == "solid"], style="solid")
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if d["style"] == "dashed"], style="dashed")
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if d["style"] == "curved"], 
                             connectionstyle="arc3,rad=0.3", edge_color="red")
        plt.title("Planning Graph")
        plt.savefig("planning_graph.png")
        plt.close()
