import asyncio
from asyncua import Client

import time
#tart = time.time()
#nd = time.time()
#rint(end - start)


url = "opc.tcp://34.142.142.99:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"

async def main():
    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        temp_node = await client.nodes.root.get_child(
            f"0:Objects/{nsidx}:/{nsidx}:temperature"
        )

        # Read value
        # cur_val = await temp_node.read_value()
        # print(f"Current value is {cur_val}")
        while(True):
            # Write value
            new_val = 28
            await temp_node.write_value(new_val)
            print(f"Updated value to {new_val}")
            time.sleep(20)
            
if __name__ == "__main__":
    asyncio.run(main())
