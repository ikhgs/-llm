from flask import Flask, request, jsonify
import replicate
import os

app = Flask(__name__)

# Configure the Replicate client with the API token
replicate_client = replicate.Client(api_token=os.getenv('REPLICATE_API_TOKEN'))

@app.route('/', methods=['GET'])
def ask():
    try:
        # Récupérer les paramètres de la chaîne de requête
        prompt = request.args.get('ask', 'Default prompt')
        title = "🍟Bruno🍟"
        result = ''

        # Utiliser la méthode 'create' pour générer une réponse unique
        response = replicate_client.predictions.create(
            version="meta/meta-llama-3.1-405b-instruct",
            input={"prompt": prompt}
        )

        # Attendre la fin de la prédiction
        response.wait()

        if response.status == "succeeded":
            result = response.output
        else:
            result = f"Error: {response.error}"

        # Structurer la réponse JSON avec le titre et le contenu généré
        response_json = {
            "title": title,
            "content": result
        }

        # Retourner le résultat structuré sous forme de JSON
        return jsonify(response_json)

    except Exception as e:
        # Handle exceptions and return a JSON response with the error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Écoute sur le port 5000 (ou tout autre port que vous souhaitez)
    app.run(host='0.0.0.0', port=5000)
