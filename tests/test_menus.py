import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.menus._menu import Menu
from src.menus._landing import Landing
from src.menus.topic._topic import TopicMenu
from src.menus.topic._embeddings import EmbeddingsMenu
from src.menus.topic._dim_red import DimensionalityReductionMenu
from src.menus.topic._cluster import ClusterMenu
from src.menus.topic._fine_tune import FineTuneMenu
from src.menus.topic._plotting import TopicPlottingMenu
from src.menus.optimization._optimization import OptimizationMenu
from src.menus.optimization._section import SectionMenu
from src.menus.optimization._plotting import OptimizationPlottingMenu
from src.menus.optimization._scoring import ScoringMenu
from src.menus.optimization._method_bayesian import BayesianMenu
from src.menus.optimization._method_grid import GridSearchMenu
def test_constructor():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    assert menu.options == ["Option 1", "Option 2", "Option 3", "Back", "Exit"]
    assert menu.is_leaf == False

def test_setters():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    menu.options = ["Option 4", "Option 5", "Option 6"]
    assert menu.options == ["Option 4", "Option 5", "Option 6"]
    menu.is_leaf = True
    assert menu.is_leaf == True

def test_display():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    display = menu.display()
    assert display == ["1. Option 1", "2. Option 2", "3. Option 3", "4. Back", "5. Exit"]

def test_get_choice_no_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    choice = menu.get_choice(1)
    assert choice == 0

def test_get_choice_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], True)
    choice = menu.get_choice(1)
    assert choice == "Option 1"
    choice = menu.get_choice(3)
    assert choice == "Option 3"
    choice = menu.get_choice(4)
    assert choice == "Back"

def test_landing():
    landing = Landing()
    assert landing.options == [
        "Run a Topic Model",
        "Run an Optimization routine for a Topic Model (GPU reccomended)",
        "Load Global Data",
        "Load Global Topic Model Configuration",
        "Load Global Optimization Configuration",
        "Exit"
    ]
    assert landing.is_leaf == False
    assert landing.is_root == True
    display = landing.display()
    assert display == [
        "1. Run a Topic Model",
        "2. Run an Optimization routine for a Topic Model (GPU reccomended)",
        "3. Load Global Data",
        "4. Load Global Topic Model Configuration",
        "5. Load Global Optimization Configuration",
        "6. Exit"
    ]
    choice = landing.get_choice(1)
    assert choice == 0
    choice = landing.get_choice(6)
    assert choice == 5

def test_topic():
    topic = TopicMenu()
    assert topic.options == [
        "Load Data",
        "Load Configuration",
        "Select LLM to generate Embeddings",
        "Select Dimensionality Reduction Technique",
        "Select Clustering Technique",
        "Fine Tuning",
        "Plotting",
        "Saving",
        "Run Topic Model",
        "Back",
        "Exit"
    ]
    assert topic.is_leaf == False
    assert topic.is_root == False
    display = topic.display()
    assert display == [
        "1. Load Data",
        "2. Load Configuration",
        "3. Select LLM to generate Embeddings",
        "4. Select Dimensionality Reduction Technique",
        "5. Select Clustering Technique",
        "6. Fine Tuning",
        "7. Plotting",
        "8. Saving",
        "9. Run Topic Model",
        "10. Back",
        "11. Exit"
    ]
    choice = topic.get_choice(1)
    assert choice == 0
    choice = topic.get_choice(10)
    assert choice == 9
    
def test_cluster():
    cluster = ClusterMenu()
    assert cluster.options == [
        "hdbscan",
        "kmeans",
        "spectral clustering",
        "dbscan",
        "agglomerative clustering",
        "birch",
        "affinity propagation",
        "mean shift",
        "Back",
        "Exit"
    ]
    assert cluster.is_leaf == True
    assert cluster.is_root == False
    display = cluster.display()
    assert display == [
        "1. hdbscan",
        "2. kmeans",
        "3. spectral clustering",
        "4. dbscan",
        "5. agglomerative clustering",
        "6. birch",
        "7. affinity propagation",
        "8. mean shift",
        "9. Back",
        "10. Exit"
    ]
    choice = cluster.get_choice(1)
    assert choice == "hdbscan"
    choice = cluster.get_choice(10)
    assert choice == "Exit"

def test_embeddings():
    embeddings = EmbeddingsMenu()
    assert embeddings.options == [
        "all-MiniLM-L6-v2",
        "all-MiniLM-L12-v2",
        "Muennighoff/SGPT-125M-weightedmean-msmarco-specb-bitfit",
        "Muennighoff/SGPT-125M-weightedmean-nli-bitfit",
        "multi-qa-MiniLM-L6-cos-v1",
        "all-mpnet-base-v2",
        "Muennighoff/SGPT-1.3B-weightedmean-msmarco-specb-bitfit",
        "Back",
        "Exit"
    ]
    assert embeddings.is_leaf == True
    assert embeddings.is_root == False
    display = embeddings.display()
    assert display == [
        "1. all-MiniLM-L6-v2",
        "2. all-MiniLM-L12-v2",
        "3. Muennighoff/SGPT-125M-weightedmean-msmarco-specb-bitfit",
        "4. Muennighoff/SGPT-125M-weightedmean-nli-bitfit",
        "5. multi-qa-MiniLM-L6-cos-v1",
        "6. all-mpnet-base-v2",
        "7. Muennighoff/SGPT-1.3B-weightedmean-msmarco-specb-bitfit",
        "8. Back",
        "9. Exit"
    ]
    choice = embeddings.get_choice(1)
    assert choice == "all-MiniLM-L6-v2"
    choice = embeddings.get_choice(9)
    assert choice == "Exit"

def test_dim_red():
    dim_red = DimensionalityReductionMenu()
    assert dim_red.options == [
        "UMAP",
        "PCA",
        "t-SNE",
        "Truncated SVD",
        "Factor Analysis",
        "Back",
        "Exit"
    ]
    assert dim_red.is_leaf == True
    assert dim_red.is_root == False
    display = dim_red.display()
    assert display == [
        "1. UMAP",
        "2. PCA",
        "3. t-SNE",
        "4. Truncated SVD",
        "5. Factor Analysis",
        "6. Back",
        "7. Exit"
    ]
    choice = dim_red.get_choice(1)
    assert choice == "UMAP"
    choice = dim_red.get_choice(7)
    assert choice == "Exit"

def test_fine_tune():
    finetune = FineTuneMenu()
    assert finetune.options == [
        "Enable 2-grams",
        "Enable 3-grams",
        "Ignore Words",
        "Enable BM25 weighting",
        "Reduce frequent words",
        "Enable KeyBERT algorithm",
        "Enable ZeroShotClassification",
        "Enable Maximal Marginal Relevance",
        "Enable Part of Speech filtering",
        "Back",
        "Exit"
    ]
    assert finetune.is_leaf == True
    assert finetune.is_root == False
    display = finetune.display()
    assert display == [
        "1. Enable 2-grams",
        "2. Enable 3-grams",
        "3. Ignore Words",
        "4. Enable BM25 weighting",
        "5. Reduce frequent words",
        "6. Enable KeyBERT algorithm",
        "7. Enable ZeroShotClassification",
        "8. Enable Maximal Marginal Relevance",
        "9. Enable Part of Speech filtering",
        "10. Back",
        "11. Exit"
    ]
    choice = finetune.get_choice(1)
    assert choice == "Enable 2-grams"
    choice = finetune.get_choice(11)
    assert choice == "Exit"

def test_optimization():
    optimization = OptimizationMenu()
    assert optimization.options == [
        "Choose a section to optimize",
        "Choose a scoring function",
        "Enable Bayesian Optimization",
        "Choose a heuristic for optimization",
        "Configure Hyperparameter Distributions",
        "Configure Plotting",
        "Run Optimization",
        "Back",
        "Exit"
    ]
    assert optimization.is_leaf == False
    assert optimization.is_root == False
    display = optimization.display()
    assert display == [
        "1. Choose a section to optimize",
        "2. Choose a scoring function",
        "3. Enable Bayesian Optimization",
        "4. Choose a heuristic for optimization",
        "5. Configure Hyperparameter Distributions",
        "6. Configure Plotting",
        "7. Run Optimization",
        "8. Back",
        "9. Exit"
    ]
    choice = optimization.get_choice(1)
    assert choice == 0
    choice = optimization.get_choice(9)
    assert choice == 8


def test_section():
    section = SectionMenu()
    assert section.options == [
        "LLM",
        "Dimensionality Reduction",
        "Clustering",
        "Back",
        "Exit"
    ]
    assert section.is_leaf == True
    assert section.is_root == False
    display = section.display()
    assert display == [
        "1. LLM",
        "2. Dimensionality Reduction",
        "3. Clustering",
        "4. Back",
        "5. Exit"
    ]
    choice = section.get_choice(1)
    assert choice == "LLM"
    choice = section.get_choice(5)
    assert choice == "Exit"

def test_topic_plotting():
    topic_plotting = TopicPlottingMenu()
    assert topic_plotting.options == [
        "Visualize Topics",
        "Visualize Documents",
        "Visualize Document Hierarchy",
        "Visualize Topic Hierarchy",
        "Visualize Topic Tree",
        "Visualize Topic Terms",
        "Visualize Topic Similarity",
        "Visualize Term Score Decline",
        "Visualize Topic Probability Distribution",
        "Visualize Topics over Time",
        "Visualize Topics per Class",
        "Back",
        "Exit"
    ]
    assert topic_plotting.is_leaf == True
    assert topic_plotting.is_root == False
    display = topic_plotting.display()
    assert display == [
        "1. Visualize Topics",
        "2. Visualize Documents",
        "3. Visualize Document Hierarchy",
        "4. Visualize Topic Hierarchy",
        "5. Visualize Topic Tree",
        "6. Visualize Topic Terms",
        "7. Visualize Topic Similarity",
        "8. Visualize Term Score Decline",
        "9. Visualize Topic Probability Distribution",
        "10. Visualize Topics over Time",
        "11. Visualize Topics per Class",
        "12. Back",
        "13. Exit"
    ]
    choice = topic_plotting.get_choice(1)
    assert choice == "Visualize Topics"
    choice = topic_plotting.get_choice(13)
    assert choice == "Exit"

def test_optimization_plotting():
    optimization_plotting = OptimizationPlottingMenu()
    assert optimization_plotting.options == [
        "Plot Convergence",
        "Plot Evaluations",
        "Plot Objective",
        "Back",
        "Exit"
    ]
    assert optimization_plotting.is_leaf == True
    assert optimization_plotting.is_root == False
    display = optimization_plotting.display()
    assert display == [
        "1. Plot Convergence",
        "2. Plot Evaluations",
        "3. Plot Objective",
        "4. Back",
        "5. Exit"
    ]
    choice = optimization_plotting.get_choice(1)
    assert choice == "Plot Convergence"
    choice = optimization_plotting.get_choice(5)
    assert choice == "Exit"

def test_scoring():
    scoring = ScoringMenu()
    assert scoring.options == [
        'silhouette_score',
        'calinski_harabasz_score',
        'davies_bouldin_score',
        'composite (all)',
        "Back",
        "Exit"
    ]
    assert scoring.is_leaf == True
    assert scoring.is_root == False
    display = scoring.display()
    assert display == [
        "1. silhouette_score",
        "2. calinski_harabasz_score",
        "3. davies_bouldin_score",
        "4. composite (all)",
        "5. Back",
        "6. Exit"
    ]
    choice = scoring.get_choice(1)
    assert choice == "silhouette_score"
    choice = scoring.get_choice(6)
    assert choice == "Exit"

def test_bayesian():
    bayesian = BayesianMenu()
    assert bayesian.options == [
        'Random Forest',
        'Gradient Boosting',
        'Gaussian Process',
        "Back",
        "Exit"
    ]
    assert bayesian.is_leaf == True
    assert bayesian.is_root == False
    display = bayesian.display()
    assert display == [
        "1. Random Forest",
        "2. Gradient Boosting",
        "3. Gaussian Process",
        "4. Back",
        "5. Exit"
    ]
    choice = bayesian.get_choice(1)
    assert choice == "Random Forest"
    choice = bayesian.get_choice(5)
    assert choice == "Exit"

def test_grid_search():
    grid_search = GridSearchMenu()
    assert grid_search.options == [
        'Enable Successive Halving',
        'Enable Random Search',
        'Greedy',
        'Random Walk',
        'Genetic Algorithm',
        "Back",
        "Exit"
    ]
    assert grid_search.is_leaf == True
    assert grid_search.is_root == False
    display = grid_search.display()
    assert display == [
        "1. Enable Successive Halving",
        "2. Enable Random Search",
        "3. Greedy",
        "4. Random Walk",
        "5. Genetic Algorithm",
        "6. Back",
        "7. Exit"
    ]
    choice = grid_search.get_choice(1)
    assert choice == "Enable Successive Halving"
    choice = grid_search.get_choice(7)
    assert choice == "Exit"