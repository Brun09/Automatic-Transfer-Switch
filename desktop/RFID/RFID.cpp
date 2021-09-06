#include "Header.h"
#include "RFID.h"

void RFID::criaRFID()
{

	CPhidgetRFIDHandle rfid = 0;
	CPhidgetRFID_create(&rfid);


}

int CCONV RFID::attachHandler(CPhidgetHandle RFID, void *userPtr)
{

	int serialNo;
	const char *name;

	CPhidget_getDeviceName(RFID, &name);
	CPhidget_getSerialNumber(RFID, &serialNo);
	cout << name << serialNo << "Ligado" << endl;

	return 0;
}


int CCONV RFID::dettachHandler(CPhidgetHandle RFID, void *userptr)
{

	int serialNo;
	const char *name;

	CPhidget_getDeviceName(RFID, &name);
	CPhidget_getSerialNumber(RFID, &serialNo);
	cout << name << serialNo << "Desligado" << endl;

	return 0;

}

int CCONV RFID::errorHandler(CPhidgetHandle RFID, void *userptr, int ErrorCode, const char *unknown)
{
	cout << "Erro manipulado." << ErrorCode << unknown << endl;
	return 0;
}

int CCONV RFID::TagHandler(CPhidgetRFIDHandle RFID, void *usrptr, char *TagVal, CPhidgetRFID_Protocol proto)
{
	//Liga o led da placa
	CPhidgetRFID_setLEDOn(RFID, 1);
	cout << "leitura da Tag" << TagVal << endl;

	return 0;
}

int CCONV RFID::TagLostHandler(CPhidgetRFIDHandle RFID, void *usrptr, char *TagVal, CPhidgetRFID_Protocol proto)
{
	//turn off the Onboard LED
	CPhidgetRFID_setLEDOn(RFID, 0);

	cout << "Tag perdida" << TagVal << endl;

	return 0;
}

