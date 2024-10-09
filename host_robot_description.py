from aiohttp import web
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--package_root', type=str, required=True)
    parser.add_argument('--urdf_relpath', type=str, required=True)
    parser.add_argument('--yaml_relpath', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    app = web.Application()
    app.add_routes([
        web.static('/robot_description/', args.package_root),
        web.get('/urdf_location/', lambda request: web.Response(text=args.urdf_relpath)),
        web.get('/yaml_location/', lambda request: web.Response(text=args.yaml_relpath)),
    ])
    
    # Turn off CORS
    async def on_prepare(request, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
    
    app.on_response_prepare.append(on_prepare)
    
    web.run_app(app, port=args.port)