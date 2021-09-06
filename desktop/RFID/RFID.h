#include "Header.h"

class RFID
{

	protected:
		RFID();
		~RFID();
		void criaRFID();
		int CCONV attachHandler(CPhidgetHandle);
		int CCONV dettachHandler(CPhidgetHandle);
		int CCONV errorHandler(CPhidgetHandle, int, const char);
		int CCONV TagHandler(CPhidgetRFIDHandle, char, CPhidgetRFID_Protocol);
		int CCONV TagLostHandler(CPhidgetRFIDHandle, char, CPhidgetRFID_Protocol);

};

