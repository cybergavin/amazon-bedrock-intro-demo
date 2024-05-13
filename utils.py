import boto3
import pandas as pd
import numpy as np
import json
from langchain.embeddings import BedrockEmbeddings

# Create bedrock boto3 clients
bedrock = boto3.client(service_name='bedrock')
bedrock_runtime = boto3.client(service_name='bedrock-runtime')
# Create bedrock_embeddings instance using LangChain
bedrock_embeddings = BedrockEmbeddings(client=bedrock_runtime)


def list_bedrock_fm_ids(input_modality:list =  ['ALL'],
                        output_modality:list =  ['ALL'],
                        inference_type:list = ['ALL']
                        ):
  """
  List all available Bedrock foundation model IDs that match the given input/output modalities and
    inference type. The default value for these parameters is ['ALL'] which ignores filtering.
  """
  # Remove 'ALL' from parameter values to avoid filtering on 'ALL'
  for parameter in [input_modality, output_modality, inference_type]:
    if 'ALL' in parameter:
      parameter.remove('ALL')

  # List all Bedrock FMs
  models = bedrock.list_foundation_models()['modelSummaries']
  modelids = []

  # Loop through each model and check if it matches the given filter parameters
  for m in models:
    input_check = True
    if input_modality:  
      input_check = all(mode in m['inputModalities'] for mode in input_modality)
    output_check = True
    if output_modality:
      output_check = all(mode in m['outputModalities'] for mode in output_modality)
    inference_check = True  
    if inference_type:
      inference_check = all(inf_type in m['inferenceTypesSupported'] for inf_type in inference_type)
    if input_check and output_check and inference_check:
      modelids.append(m['modelId'])
  return modelids


def colorize_rows(row, color_map):
    """Function to return color style for dataframe row."""
    color = color_map.get(row['Provider'], "#D4ECF9")  # Default to light blue if no match found
    return ['background-color: %s' % color] * len(row)  # Apply to all columns


def generate_bedrock_fm_table():
    """
    Generate a table of all available Bedrock foundation models.
    """
    models = bedrock.list_foundation_models()['modelSummaries']
    
    # Dictionary of lists where each list represents a row in the table
    provider_name = []
    model_name = []
    model_id = []
    input_modalities = []
    output_modalities = []
    inference_types = []
    customizations = []

    for m in models:
        provider_name.append(m['providerName'])
        model_name.append(m['modelName'])
        model_id.append(m['modelId'])
        input_modalities.append(m['inputModalities'])
        output_modalities.append(m['outputModalities'])
        inference_types.append(m['inferenceTypesSupported'])
        customizations.append(m['customizationsSupported'])

    data = {
        "Provider": provider_name,
        "Model": model_name,
        "Model ID": model_id,
        "Input Modalities": input_modalities,
        "Output Modalities": output_modalities,
        "Inference Types": inference_types,
        "Customizations": customizations
    }

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(data)

    # Define a color map based on unique provider names using only two light shades
    unique_names = df['Provider'].unique()
    light_shades = ['#D4ECF9', '#F1FADD']  # Two different light shades
    color_map = {name: light_shades[i % 2] for i, name in enumerate(unique_names)}
    
    return df, unique_names, color_map

    
def ask_fm(modelid:str, prompt:str) -> str:
    """Invoke specific FM using boto3 and pass prompt and max tokens - all other inference parameters will use default values"""
    unsupported = False
    accept = "application/json"
    contentType = "application/json"
    if "ai21.j2" in modelid:
        body = json.dumps(
            {
                "prompt": prompt,
                "maxTokens": 1024
            }
        )
    elif "anthropic.claude" in modelid:
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": f"{prompt}"}]
            }
        )
    elif "cohere.command-r" in modelid:
        body = json.dumps(
            {
                "message": prompt,
                "max_tokens": 1024
            }
        )
    elif "cohere.command-text" in modelid or "cohere.command-light" in modelid:
        body = json.dumps(
            {
                "prompt": prompt,
                "max_tokens": 1024
            }
        )
    elif "meta" in modelid:
        body = json.dumps(
            {
                "prompt": prompt,
                "max_gen_len": 1024
            }
        )
    elif "mistral" in modelid:
        body = json.dumps(
            {
                "prompt": f"""<s>[INST] {prompt} [/INST]""",
                "max_tokens": 1024
            }
        )            
    elif "amazon" in modelid:
        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1024
                    }
            }
        )
    else:
        unsupported = True
    
    if unsupported:
        return f"Unsupported model. This application's code must be modified for inferencing with {modelid}", None, None
    else:
        # Invoke FM
        response = bedrock_runtime.invoke_model(body=body, modelId=modelid, accept=accept, contentType=contentType)
        # Parse and print output
        response_body = json.loads(response["body"].read())
        if "ai21.j2" in modelid:
            return response_body["completions"][0]["data"]["text"], None, None
        elif "anthropic.claude" in modelid:
            return response_body['content'][0]['text'], response_body['usage']['input_tokens'], response_body['usage']['output_tokens']
        elif "cohere.command-r-" in modelid:
            return response_body["text"], None, None
        elif "cohere.command-text" in modelid or "cohere.command-light" in modelid:
            return response_body['generations'][0]['text'], None, None
        elif "meta" in modelid:
            return response_body["generation"], response_body['prompt_token_count'], response_body['generation_token_count']
        elif "amazon" in modelid:
            return response_body["results"][0]["outputText"], response_body["inputTextTokenCount"], response_body["results"][0]["tokenCount"]
        elif "mistral" in modelid:
            return response_body['outputs'][0]['text'], None, None