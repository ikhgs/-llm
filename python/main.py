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
        result = ''
        max_length = 5000  # Par exemple, ajustez cette valeur selon les capacités de l'API
        continue_generating = True
        title = "🍟Bruno🍟"

        while continue_generating:
            # Stream des résultats
            for event in replicate_client.models.get("meta/meta-llama-3.1-405b-instruct").stream(
                input={"prompt": prompt, "max_length": max_length},
            ):
                result += str(event)

            # Vérifier si la réponse est terminée ou si elle doit être étendue
            if len(result) < max_length:
                continue_generating = False
            else:
                # Mettre à jour le prompt pour inclure le résultat généré jusqu'à présent
                prompt = result[-max_length:]

        # Structurer la réponse JSON avec le titre et le contenu généré
        response = {
            "title": title,
            "content": result
        }

        # Retourner le résultat structuré sous forme de JSON
        return jsonify(response)

    except Exception as e:
        # Handle exceptions and return a JSON response with the error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Écoute sur le port 5000 (ou tout autre port que vous souhaitez)
    app.run(host='0.0.0.0', port=5000)
