from diffusers import DiffusionPipeline
import torch

class StableDifussionXL():

    def __init__(self, refiner=False, mem_offload=False):
        """
        Initialize the StableDiffusionXL class.

        :param refiner: boolean, If True, a refiner model will be initialized along with the base model.
        :param mem_offload: boolean, If True, model's weights are loaded into CPU memory and then moved to GPU memory only during inference to save GPU memory.
        """

        if not isinstance(refiner, bool):
            raise TypeError('refiner must be a boolean')
        if not isinstance(mem_offload, bool):
            raise TypeError('menm_offload must be a boolean')
        
        self._base = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", 
                                                       torch_dtype=torch.float16, variant="fp16", 
                                                       use_safetensors=True
                                                       )
    
        if mem_offload:
            self._base.enable_model_cpu_offload()
        else:
            self._base.to("cuda")

        self._refiner = None
        
        if refiner:
            self._refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0", 
                                                              text_encoder_2=self._base.text_encoder_2, 
                                                              vae=self._base.vae, 
                                                              torch_dtype=torch.float16, 
                                                              use_safetensors=True, 
                                                              variant="fp16",
                                                              )
            if mem_offload:
                self._refiner.enable_model_cpu_offload()
            else:
                self._refiner.to("cuda")

    def infer(self, prompt, negative_prompt, use_refiner=False, n_steps=40, high_noise_frac=0.8):
        """
        Perform inference using the models.

        :param prompt: str, Primary input prompt for model inference.
        :param negative_prompt: str, Negative prompt used to guide the model in avoiding certain outputs.
        :param use_refiner: boolean, If True and if a refiner model is available, it will be used for refinement.
        :param n_steps: int, Number of inference steps.
        :param high_noise_frac: float, Fraction at which the refiner starts denoising.
        :return: Image object, Resulting generated image.
        """
        
        if not isinstance(prompt, str) or not isinstance(prompt, str):
            raise TypeError('prompts must be str')
        if not isinstance(use_refiner, bool):
            raise TypeError('use_refiner must be a boolean')

        model_text = "Image generated using: "
        use_refiner = (self._refiner is not None) and use_refiner

        print("Base model:")
        image = self._base(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=n_steps,
            denoising_end= None if (not use_refiner) else high_noise_frac,
            output_type= "pil" if (not use_refiner) else "latent",
            ).images
        model_text += "base "

        if (use_refiner):
            print("Refiner model:")
            torch.cuda.empty_cache()
            image = self._refiner(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=n_steps,
                    denoising_start=high_noise_frac,
                    image=image,
                    ).images
            model_text += "refiner"
        print(model_text)
        return image