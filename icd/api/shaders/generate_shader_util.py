##
 #######################################################################################################################
 #
 #  Copyright (c) 2017-2023 Advanced Micro Devices, Inc. All Rights Reserved.
 #
 #  Permission is hereby granted, free of charge, to any person obtaining a copy
 #  of this software and associated documentation files (the "Software"), to deal
 #  in the Software without restriction, including without limitation the rights
 #  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 #  copies of the Software, and to permit persons to whom the Software is
 #  furnished to do so, subject to the following conditions:
 #
 #  The above copyright notice and this permission notice shall be included in all
 #  copies or substantial portions of the Software.
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.
 #
 #######################################################################################################################

#**********************************************************************************************************************
# @file  make_llpc_shaders.py
# @brief LLPC python script file: generates SPIR-V binary for internal pipelines
#**********************************************************************************************************************

"""Module providing utility functions to compile shaders and generate their corresponding spv include files"""
import binascii
import os
import subprocess
import sys

def is_64_bit():
    """Function to check if environment is 64 bit"""
    # https://docs.python.org/2/library/sys.html#sys.maxsize
    # https://docs.python.org/2/library/platform.html#cross-platform
    return sys.maxsize > 2**32

vulkanSDK = os.getenv("VULKAN_SDK")

if vulkanSDK is None:
    sys.exit("Specify path to Vulkan SDK by setting VULKAN_SDK enviroment variable.")

glslangValidator = os.path.join(vulkanSDK, "bin" if is_64_bit() else "Bin32", "glslangValidator")

def generate_spv_header_file(in_file, out_file, marco_def):
    """Functioin to generate the SPIR-V header file"""
    # Generate spv file
    print(">>>  (glslangValidator) " + in_file + " ==> " + out_file + ".spv")
    cmd_line = "glslangValidator -V " + in_file + " "+ marco_def + " -o " + out_file + ".spv"
    subprocess.call(cmd_line, shell = True)

    # Convert .spv file to a hex file
    spv_file = out_file + ".spv"
    h_file = out_file +"_spv.h"
    print(">>>  (bin2hex) " + spv_file + "  ==>  " + h_file)
    f_bin = open(spv_file, "rb")
    bin_data = f_bin.read()
    f_bin.close()

    hex_data = binascii.hexlify(bin_data).decode()
    f_hex = open(h_file, "w")
    hex_text = "// do not edit by hand; created from source file " + in_file + \
    " by executing script generate_shader_util.py\n"
    i = 0
    while i < len(hex_data):
        hex_text += "0x"
        hex_text += hex_data[i]
        hex_text += hex_data[i + 1]
        i += 2
        if (i != len(hex_data)):
            hex_text += ", "
        if (i % 32 == 0):
            hex_text += "\n"
    f_hex.write(hex_text)
    f_hex.close()

    # Remove the .spv file that was generated by glslang
    os.remove(spv_file)
