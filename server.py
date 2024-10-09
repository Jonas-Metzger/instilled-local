import asyncio
import json
from websockets.server import serve


class Server:
    def __init__(self, robots):
        self.robots = robots
        self.websocket = None
        self.file_server = None

    async def record_joints(self, websocket):
        self.websocket = websocket
        print("connection received")
        async for message in websocket:
            data = json.loads(message)
            if 'joint_states' in data:
                for robot in self.robots:
                    for joint_name, joint_value in data['joint_states'].items():
                        if joint_name in robot.joints:
                            robot.joint_states[joint_name] = joint_value

    async def host_robot_description(self, package_root, urdf_relpath, yaml_relpath, port):
        print(f"hosting {package_root} at http://localhost:{port}/robot_description")
        print(f"NOTE: any filepaths in the URDF must start with 'package://', which which should refer to the folder: {package_root}/")
        self.file_server = await asyncio.create_subprocess_shell(
            f"python host_robot_description.py --package_root {package_root} --urdf_relpath {urdf_relpath} --yaml_relpath {yaml_relpath} --port {port}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await self.file_server.communicate()
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    async def serve(self, sync_joints_every_ms, package_root=None, urdf_relpath=None, yaml_relpath=None):
        print(f"syncing joints every {sync_joints_every_ms}ms, feel free to adjust")
        async with serve(self.record_joints, "localhost", 9090):
            print("started websocket server.")
            coroutines = [robot.sync_joints(sync_joints_every_ms) for robot in self.robots]
            if package_root is not None:
                coroutines.append(self.host_robot_description(package_root, urdf_relpath, yaml_relpath, 9091))
            await asyncio.gather(*coroutines)


class Robot:
    def __init__(self):
        self.joints = []
        self.joint_states = {}
        self.lock = asyncio.Lock()

    async def send_joint(self, joint_name, joint_value):
        raise NotImplementedError("This is a base class")

    async def sync_joints(self, every_ms):
        while True:
            await self.lock.acquire() # this prevents race conditions
            for joint_name, joint_value in self.joint_states.items():
                await self.send_joint(joint_name, joint_value)
            self.lock.release()
            await asyncio.sleep(every_ms/1000)



################################################################################
# Implement Your Robots Here
################################################################################
class MarcelArm(Robot):
    def __init__(self):
        super().__init__()
        self.joints = ["joint0", "joint1", "joint2", "joint3", "joint4", "joint5"]
    
    async def send_joint(self, joint_name, joint_value):
        print(f"setting joint {joint_name} to {joint_value}")
        # TODO: implement sending joint to robot via its python api
        # if your robot's python api does not support async, make sure to wrap it as
        # await asyncio.to_thread(some_non_async_function, *its_arguments)


class WX250S(Robot):
    def __init__(self):
        super().__init__()
        self.joints = ["waist", "shoulder", "elbow", "forearm_roll", "wrist_angle", "wrist_rotate", "left_finger"]
    
    async def send_joint(self, joint_name, joint_value):
        print(f"setting joint {joint_name} to {joint_value}")
        # TODO: implement sending joint to robot via its python api
        # if your robot's api does not support async, make sure to wrap it as
        # await asyncio.to_thread(some_non_async_function, *its_arguments)

################################################################################


if __name__ == "__main__":
    robots = [MarcelArm(), WX250S()]
    server = Server(robots)
    try:
        asyncio.run(server.serve(
            sync_joints_every_ms=1000,

            package_root="robot_descriptions/marcel_plus_wx250s",
            urdf_relpath="urdf/bimanual.urdf",
            yaml_relpath="urdf/bimanual.yaml"

            #package_root="robot_descriptions/wx250s",
            #urdf_relpath="urdf/wx250s.urdf",
            #yaml_relpath="urdf/wx250s.yaml"

            #package_root="robot_descriptions/marcel_arm",
            #urdf_relpath="marcel_arm.urdf",
            #yaml_relpath="marcel_arm.yaml"    

            #package_root="robot_descriptions/mycobot_280_m5",
            #urdf_relpath="mycobot_280m5_bimanual.urdf",
            #yaml_relpath="mycobot_280m5_bimanual.yaml"
        ))
    except KeyboardInterrupt:
        if server.file_server is not None:
            server.file_server.terminate()
        print("Shutting down server...")
