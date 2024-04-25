from src.obj._finetuner import FineTuner


class TunerFactory:
    @staticmethod
    def create_tuner(
        model_filepath: str = "",
        data_filepath: str = "",
        prompt: str = "",
        format="",
        output_path: str = "",
        lora_params: dict = {},
        training_params: dict = "",
    ):
        return FineTuner(
            model_filepath,
            data_filepath,
            prompt,
            format,
            output_path,
            lora_params,
            training_params,
        )
