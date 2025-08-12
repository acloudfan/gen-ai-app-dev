# The Hugging Face endpoints expose model as API
# These models take keyword arguments depending on the task
# These are kwargs for text-generation task
# https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task

model_kwargs_textgen ={
    # (Default: None). Integer to define the top tokens 
    #considered within the sample operation to create new text.
    'top_k'	: None, 

    # (Default: None). Float to define the tokens that are within the sample operation of 
    # text generation. Add tokens in the sample for more probable to least probable until 
    # the sum of the probabilities is greater than top_p.
    'top_p'	: None,

    # (Default: 1.0). Float (0.0-100.0). The temperature of the sampling operation. 1 means 
    # regular sampling, 0 means always take the highest score, 100.0 is getting closer to uniform probability.
    'temperature' : 0,

    # (Default: None). Float (0.0-100.0). The more a token is used within generation the more it is penalized 
    # to not be picked in successive generation passes.
    'repetition_penalty' : None,

    # (Default: None). Int (0-250). The amount of new tokens to be generated, this does not include the input 
    # length it is a estimate of the size of generated text you want. Each new tokens slows down the request, 
    # so look for balance between response times and length of text generated.
    'max_new_tokens' : None,

    # (Default: None). Float (0-120.0). The amount of time in seconds that the query should take maximum. Network 
    # can cause some overhead so it will be a soft limit. Use that in combination with max_new_tokens for best results.
    'max_time' : None,

    # (Default: True). Bool. If set to False, the return results will not contain the original query making 
    # it easier for prompting.
    'return_full_text' : True,

    # (Default: 1). Integer. The number of proposition you want to be returned.
    'num_return_sequences' : 1,

    # (Optional: True). Bool. Whether or not to use sampling, use greedy decoding otherwise.
    'do_sample' : True,

    #### The last 2 parameters control the behavior of the Endpoint not the model ####

    # API uses cache, so if input is re-used, response is picked from cache instead of enpoint invocation
    'use_cache' : True,

    # (Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. 
    # It limits the number of requests required to get your inference done. It is advised to only 
    # set this flag to true after receiving a 503 error as it will limit hanging in your application to known places.
    'wait_for_model' : False
}

# Checks if there is any unknown parameter in the args
def  validate_hf_arguments(params):
    for key in params:
        if key not in model_kwargs:
            raise ValueError("{key} is not a valid parameter for Hugging Face text generation models!!")