import mysql.connector
import json
import menu


class Dbfunction():
    def __init__(self) -> None:
        super().__init__()


    vistradb_config = menu.getJsonVal("env_var", "vistradb_config")
    stsportal_config = menu.getJsonVal("env_var", "stsportal_config")
    cptsiac_config = menu.getJsonVal("env_var", "cptsiac_config")

    def execute_query(self, query_config, query_stm, fetchAll=True, ReturnType=1, firstRow=''):
        try:
            # Connect to the MySQL server
            connection = mysql.connector.connect(**query_config)

            # Create a cursor object to execute queries
            cursor = connection.cursor()

            cursor.execute(query_stm)
            column_names = [col[0] for col in cursor.description]
            if fetchAll:
                # Fetch the all the row from the result set
                Rows = cursor.fetchall()
                cursor.nextset()
                if not Rows:
                    allRows = [" No Data Found "]
                else:
                    if ReturnType == 1:  # Return with Col name
                        allRows = [dict(zip(column_names, row)) for row in Rows]
                        return allRows
                    elif ReturnType == 2:  # Return  for Dropdown
                        allRows = {column1_value: column2_value for column1_value, column2_value in Rows}
                        if firstRow:
                            allRows = {**{'New': firstRow}, **allRows}
                        return allRows
                    elif ReturnType == 3:  # Return  as json
                        allRows = json.dumps([dict(zip(column_names, row)) for row in Rows])
                        return allRows
                    elif ReturnType == 4:  # Flat array for Dropdown
                        allRows = [item[0] for item in Rows]
                        return allRows
                    else:
                        return Rows
            else:
                Row = cursor.fetchone()
                cursor.nextset()
                return Row

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)

        finally:
            # Close the cursor and connection
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def query_awsAcc(self, client_code):
        query_stm = f"SELECT cacc.accountnumber, cacc.description " \
                    f"FROM cld_accounts cacc " \
                    f"WHERE cacc.clientid = '{client_code}' " \
                    f"AND cacc.accountstatus = 'OPEN'"
        return self.execute_query(self.stsportal_config, query_stm, fetchAll=True, ReturnType=2)

    def query_awsRegion(self):
        query_stm = f"select ca.code,ca.name from cld_awsregions ca"

        return self.execute_query(self.stsportal_config, query_stm, True, 2)

    def query_os_type(self):
        # Placeholder for fetching OS types
        query_stm = "SELECT DISTINCT os_type FROM your_os_type_table"
        return self.execute_query(self.stsportal_config, query_stm, True, 1)

    def query_instance_type(self):
        # Placeholder for fetching instance types
        query_stm = "SELECT DISTINCT instance_type FROM your_instance_type_table"
        return self.execute_query(stsportal_config, query_stm, True, 1)
