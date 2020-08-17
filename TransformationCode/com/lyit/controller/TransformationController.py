from flask import Flask
from flask import request

from com.lyit.data.models.TransformationInput import TransformationInput
from com.lyit.service.TransformationService import TransformationService

app = Flask(__name__)


@app.route('/')
def health():
   return "success"


@app.route('/transform', methods=["POST"])
def transform():
   target_directory = None
   try:
      sourcegithuburl = request.args.get('sourcegithuburl')
      targetgithuburl = request.args.get('targetgithuburl')
      targetcloudprovider = request.args.get('targetcloudprovider')
      isDeploy = request.args.get('isDeploy')
      transformInput = TransformationInput(sourcegithuburl,
                                           targetgithuburl,
                                           targetcloudprovider,
                                           isDeploy)

      transformationService = TransformationService()
      target_directory = transformationService.transform(transformInput)
   except Exception as e:
      return "Exception occurred : " + str(e)

   if target_directory is not None:
      print("Success : code generated at : " + target_directory)
      return "Success : code generated at : " + target_directory
   else:
      print("Target Directory failed to generate!")
      return "Target Directory failed to generate!"


if __name__ == '__main__':
   app.run()