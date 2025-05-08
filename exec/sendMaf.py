#!/usr/bin/env python3
import sys
import os
import glob
import asyncio
import logging

#Uncomment this to see detailed nats messaging info.
#logging.basicConfig(level=logging.DEBUG)

# Import your handler for converting MAF to a protobuf message.
from cohort_utils.sampleprotobuf_tempoMaf import SampleProtobuf_Handler
# Import the NATS EventHandler.
from cohort_utils.nats.handler import EventHandler

def main():
    if len(sys.argv) < 2:
        print("Usage: sendMaf.py <path_to_results_directory>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    # Look for the somatic.final.maf file in the combined_mutations directory.
    maf_pattern = os.path.join(base_dir, "combined_mutations", "*.somatic.final.maf")
    maf_files = glob.glob(maf_pattern)
    
    if not maf_files:
        print("No somatic.final.maf file found in", os.path.join(base_dir, "combined_mutations"))
        sys.exit(1)
    
    maf_path = maf_files[0]
    print("Using MAF file:", maf_path)
    
    # Generate the protobuf message from the MAF file.
    maf_handler = SampleProtobuf_Handler(maf=maf_path)
    proto_message = maf_handler.generate_tempomessage()
    print("Generated protobuf message.")
    
    # Create the NATS handler for type "maf"
    # (Make sure the id_name matches your protobuf sample id field; here we use "cmoSampleId".)
    nats_handler = EventHandler(type="cbioportal", data=proto_message, id_name="cmoSampleId")
    
    # Instead of asyncio.get_event_loop(), explicitly create and set a new event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("Sending message via NATS...")
    nats_handler.send_message(loop, ignore_error=False)
    print("Message sent.")

if __name__ == "__main__":
    main()
