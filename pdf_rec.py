drive = "\\\\.\\F:"  # Open drive as raw bytes
fileD = open(drive, "rb")
size = 512         # Size of bytes to read
byte = fileD.read(size)  # Read 'size' bytes
offs = 0            # Offset location
drec = False        # Recovery mode
rcvd = 0            # Recovered file ID

while byte:
    found = byte.find(b'%PDF-')  # PDF header signature
    if found >= 0:
        drec = True
        print('==== Found PDF at location: ' + str(hex(found + (size * offs))) + ' ====')
        # Now let's create the recovered PDF file and search for the ending signature
        fileN = open(f"recovered_pdf_{rcvd}.pdf", "wb")
        fileN.write(byte[found:])
        while drec:
            byte = fileD.read(size)
            bfind = byte.find(b'%EOF')  # PDF end-of-file signature
            if bfind >= 0:
                fileN.write(byte[:bfind])
                print('==== Wrote PDF to location: recovered_pdf_' + str(rcvd) + '.pdf ====\n')
                drec = False
                rcvd += 1
                fileN.close()
            else:
                fileN.write(byte)

    byte = fileD.read(size)
    offs += 1

fileD.close()