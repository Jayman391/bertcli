from src.builders._tm_factory import TopicModelFactory
from src.builders._tu_factory import TunerFactory
from bertopic import BERTopic


class Session:
    """
    A class representing a session for topic modeling.

    Attributes:
        data (list): The data used for topic modeling.
        config_topic_model (dict): The configuration for the topic model.
        logs (dict): The logs for errors and menu choice data.
        plot_dir (str): The directory to save plots.
        topic_model_factory (TopicModelFactory): The factory for creating topic models.

    Methods:
        set_data: Set the data for topic modeling.
        set_config_topic_model: Set the configuration for the topic model.
        initialize_topic_model_factory: Initialize the topic model factory.
        get_log: Get the log.
        build_topic_model: Build the topic model.

    """

    def __init__(
        self, data=[], config_topic_model={}, config_fine_fune = {}, save_dir: str = "", data_path: str = None
    ) -> None:
        self.data = data
        self.config_topic_model = config_topic_model
        self.config_fine_tune = config_fine_fune
        self.logs = {"errors": [], "data": []}
        self.plot_dir = save_dir
        self.topic_model_factory = TopicModelFactory()
        self.tuner_factory = TunerFactory()
        self.data_path = data_path

    def set_data(self, data):
        """
        Set the data for topic modeling.

        Args:
            data (list): The data to set.

        Returns:
            list: The updated data.

        """
        self.data = data
        return self.data

    def set_config_topic_model(self, config):
        """
        Set the configuration for the topic model.

        Args:
            config (dict): The configuration to set.

        Returns:
            dict: The updated configuration.

        """
        self.config_topic_model = config
        return self.config_topic_model
    
    def set_config_fine_tune(self, config):
        """
        Set the configuration for fine tuning.

        Args:
            config (dict): The configuration to set.

        Returns:
            dict: The updated configuration.

        """
        self.config_fine_tune = config
        return self.config_fine_tune

    def initialize_topic_model_factory(self):
        """
        Initialize the topic model factory.

        Returns:
            TopicModelFactory: The initialized topic model factory.

        """
        self.topic_model_factory.upload_data(self.data)
        return self.topic_model_factory
    
    def log(self, name, log):
        self.logs[name].append(log)
    
    def get_logs(self, name):
        return self.logs[name]

    def build_topic_model(self, from_file: bool = False, config: dict = {}) -> BERTopic:
        """
        Build the topic model.

        Args:
            from_file (bool): Whether to build the topic model from file.
            config (dict): The configuration for building the topic model.

        Returns:
            BERTopic: The built topic model.

        """
        if from_file:
            self.topic_model_factory.build_embedding_model(
                self.config_topic_model["embedding_model"]
            )
            # Correct way to pass the sub-dictionary for UMAP model configuration
            umap_model_name = list(self.config_topic_model["umap_model"].keys())[0]
            umap_model_config = self.config_topic_model["umap_model"][umap_model_name]
            self.topic_model_factory.build_dim_red_model(
                umap_model_name, umap_model_config
            )

            # Correct way to pass the sub-dictionary for HDBSCAN model configuration
            hdbscan_model_name = list(self.config_topic_model["hdbscan_model"].keys())[
                0
            ]
            hdbscan_model_config = self.config_topic_model["hdbscan_model"][
                hdbscan_model_name
            ]
            self.topic_model_factory.build_cluster_model(
                hdbscan_model_name, hdbscan_model_config
            )

            self.topic_model_factory.build_vectorizer_model(
                self.config_topic_model["vectorizer_model"]
            )
            self.topic_model_factory.build_ctfidf_model(
                self.config_topic_model["ctfidf_model"]
            )
            return self.topic_model_factory.build_topic_model()
        else:
            # gather all data logs
            config = self.logs["data"]
            # get all "Embeddings" logs
            embeddings = [log for log in config if "Embeddings" in log.keys()]
            # get the most recent logged value
            if embeddings:
                embeddings = embeddings[-1]
                self.topic_model_factory.build_embedding_model(embeddings["Embeddings"])
            else:
                self.topic_model_factory.build_embedding_model()

            dim_red = [
                log for log in config if "Dimensionality Reduction" in log.keys()
            ]
            if dim_red:
                dim_red = dim_red[-1]
                self.topic_model_factory.build_dim_red_model(
                    dim_red["Dimensionality Reduction"]
                )
            else:
                self.topic_model_factory.build_dim_red_model()

            clustering = [log for log in config if "Clustering" in log.keys()]
            if clustering:
                clustering = clustering[-1]
                self.topic_model_factory.build_cluster_model(clustering["Clustering"])
            else:
                self.topic_model_factory.build_cluster_model()

            fine_tune = [log for log in config if "Fine Tuning" in log.keys()]

            vectorizer_config = {}
            ctfidf_config = {}

            for log in fine_tune:
                if log.values() == "Enable 2-grams":
                    vectorizer_config["ngram_range"] = (1, 2)
                if log.values() == "Enable 3-grams":
                    vectorizer_config["ngram_range"] = (1, 3)
                if isinstance(log.values(), list) and log.values().contains(
                    "Ignore Words"
                ):
                    words = log.values().remove("Ignore Words")
                    vectorizer_config["stop_words"] = words
                if log.values() == "Enable BM25 weighting":
                    ctfidf_config["bm25"] = True
                if log.values() == "Reduce frequent words":
                    ctfidf_config["reduce_frequent_words"] = True

            self.topic_model_factory.build_vectorizer_model(vectorizer_config)

            self.topic_model_factory.build_ctfidf_model(ctfidf_config)

            fine_tune = [list(i.values())[0] for i in fine_tune]

            self.topic_model_factory.build_fine_tune(fine_tune)

            return self.topic_model_factory.build_topic_model()

    def build_tuner(self, from_file: bool = False):
        if from_file:
            model_weights_path = self.config_fine_tune["model_weights_path"]
            training_data_path = self.config_fine_tune["train_data_path"]
            system_prompt = self.config_fine_tune["system_prompt"]
            prompt_format = self.config_fine_tune["prompt_format"]
            output_path = self.config_fine_tune["output_path"]
            learning_rate = self.config_fine_tune["learning_rate"]
            epochs = self.config_fine_tune["epochs"]
            train_test_split_ratio = self.config_fine_tune["train_test_split_ratio"]
            r = self.config_fine_tune["r"]
            alpha = self.config_fine_tune["alpha"]
        else:
            data = self.logs["data"]

            ft_data = [log for log in data if "Fine Tune" in log.keys()]

            ft_tr_data = [log for log in data if "Train" in log.keys()]

            ft_data.extend(ft_tr_data)

            for log in ft_data:
                if "weights" in log.values():
                    model_weights_path = list(log.values())[0].split(" ")[1]
                if "data" in log.values():
                    training_data_path = list(log.values())[0].split(" ")[1]
                if "system-prompt" in log.values():
                    system_prompt = str(list(log.values())[0].split(" ")[1:])
                if "prompt-format" in log.values():
                    prompt_format = list(log.values())[0].split(" ")[1]
                if "output" in log.values():
                    output_path = list(log.values())[0].split(" ")[1]
                if "learning rate" in log.values():
                    learning_rate = list(log.values())[0].split(" ")[1]
                if "epochs" in log.values():
                    epochs = list(log.values())[0].split(" ")[1]
                if "train-test-split-ratio" in log.values():
                    train_test_split_ratio = list(log.values())[0].split(" ")[1]
                if "r " in log.values():
                    r = list(log.values())[0].split(" ")[1]
                if "alpha" in log.values():
                    alpha = list(log.values())[0].split(" ")[1]
                
        lora_params = {"r": r, "alpha": alpha}
        
        training_params = {}
        if learning_rate:
            training_params["learning_rate"] = learning_rate
        if epochs:
            training_params["num_train_epochs"] = epochs
        if train_test_split_ratio:
            training_params["train_test_split_ratio"] = train_test_split_ratio

        return self.tuner_factory.create_tuner(
            model_weights_path, training_data_path, system_prompt,prompt_format, output_path, lora_params, training_params
        )