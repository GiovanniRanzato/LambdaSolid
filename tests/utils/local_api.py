from api.api_gateway.APIGatewayHandler import APIGatewayHandler

if __name__ == "__main__":
    import uvicorn
    from api.api_gateway.events.APIGatewayEventV1 import APIGatewayEventV1
    #from dotenv import load_dotenv
    # load_dotenv()
    api_handler = APIGatewayHandler(standalone=True)
    event = APIGatewayEventV1(
        event={
            "RequestContext": {
                "stage": ""
            },
            "stageVariables": {},
            "routeKey": {}
        },
        context={}
    )
    app = api_handler.handle(event)
    uvicorn.run(app, port=8080)