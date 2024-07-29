# Leverages Amazon Bedrock for accessing the LLMs
# YOU MUST have the following setup before you can use it
#   1. Amazon AWS account (Free tier, Credit card required)
#   2. Enable the models you would like to use
#   3. Boto 3 package (!pip install boto3)
#   4. Install the aws backsage for aws (!pip install -qU langchain-aws)
#   5. A local profile that has permissions to invoke LLMs


from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain_aws import ChatBedrock, BedrockEmbeddings
import boto3

# https://api.python.langchain.com/en/latest/retrievers/langchain_community.retrievers.bedrock.AmazonKnowledgeBasesRetriever.html
def  create_bedrock_knowledge_base_retriever(knowledge_base_id, 
                                             credentials_profile_name ="default", 
                                             retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}}):
    
    retriever = AmazonKnowledgeBasesRetriever(knowledge_base_id =knowledge_base_id,
                                              credentials_profile_name = credentials_profile_name,
                                              retrieval_config = retrieval_config)

    return retriever

# Chat models
# https://python.langchain.com/v0.2/docs/integrations/chat/bedrock/
# Models : https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html

def  create_bedrock_chat_model(model_id, model_kwargs={}):
    llm = ChatBedrock( model_id=model_id, model_kwargs=model_kwargs)
    return llm

# lists the models in the default region
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_foundation_models.html
def  list_bedrock_foundation_models(region=''):
    if(region == ''):
        client = boto3.client('bedrock')
    else:
        client = boto3.client('bedrock', region=region)
        
    response = client.list_foundation_models()

    model_ids=[]
    for model in response['modelSummaries']:
        model_info = {'model_name': model['modelName'], 'model_id': model['modelId']}
        model_ids.append(model_info)

    return model_ids

# https://python.langchain.com/v0.2/docs/integrations/text_embedding/bedrock/
# https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.bedrock.BedrockEmbeddings.html
def  create_bedrock_embedding_llm(model_id='amazon.titan-embed-text-v1', model_kwargs={}):
    embeddings = BedrockEmbeddings(model_id=model_id,model_kwargs=model_kwargs)
    return embeddings

