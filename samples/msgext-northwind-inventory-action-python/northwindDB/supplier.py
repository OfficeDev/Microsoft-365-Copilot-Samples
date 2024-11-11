from config import Settings
from datetime import datetime
from northwindDB.dbService import DbService
from northwindDB.model import Supplier
from datetime import datetime

async def create_supplier(self,supplier: Supplier) -> str:

    # Instantiate DbService with caching disabled
    db_service = DbService(ok_to_cache_locally=False)

    # Call get_next_id method asynchronously
    next_id = await db_service.get_next_id(Settings.TABLE_NAME["SUPPLIER"])
    
    # Entity doesn't exist, so we create it
    new_supplier = {
    "PartitionKey": Settings.TABLE_NAME["SUPPLIER"],
    "RowKey": str(next_id),
    "SupplierID": str(next_id),
    "CompanyName": supplier.CompanyName,
    "ContactName": supplier.ContactName,
    "ContactTitle": supplier.ContactTitle,
    "Address": supplier.Address,
    "City": supplier.City,
    "Region": "",
    "PostalCode": "",
    "Country": "",
    "Phone": "",
    "Fax": "",
    "HomePage": "",
    "Timestamp": datetime.now(),
    }

    await  db_service.create_entity(Settings.TABLE_NAME["SUPPLIER"],new_supplier["SupplierID"],new_supplier)
    print(f"Supplier with ID Created.")

    return new_supplier["SupplierID"]
