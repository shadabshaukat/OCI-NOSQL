import borneo
import io
import sys
import json

from fdk import response

def handler(ctx, data: io.BytesIO=None):
    err=json.dumps({"message": "Hello NoSQL"})
    try:
        print('Python Function', file=sys.stderr)
        name = "World"


        provider = borneo.iam.SignatureProvider.create_with_resource_principal()
        compartment_id = provider.get_resource_principal_claim(borneo.ResourcePrincipalClaimKeys.COMPARTMENT_ID_CLAIM_KEY)
        print('Compartment id get from claim: ' + compartment_id, file=sys.stderr)
        tenant_id = provider.get_resource_principal_claim(borneo.ResourcePrincipalClaimKeys.TENANT_ID_CLAIM_KEY)
        print('Tenant id get from claim: ' + tenant_id, file=sys.stderr)
        config = borneo.NoSQLHandleConfig('ap-sydney-1', provider).set_logger(None).set_default_compartment(compartment_id)
        store_handle = borneo.NoSQLHandle(config)
        limits = borneo.TableLimits(10, 10, 1)
        req = borneo.TableRequest().set_statement('CREATE TABLE user_eva (fld_id INTEGER, fld_str STRING, PRIMARY KEY(fld_id))').set_table_limits(limits)
        res = store_handle.do_table_request(req, 20000, 1000)
        print('Compartment id get from table result: ' + res.get_compartment_id(), file=sys.stderr)
        print('Create result: ' + str(res), file=sys.stderr)
        req = borneo.ListTablesRequest()
        res = store_handle.list_tables(req)
        tables = res.get_tables()
        #for t in tables:
            #print('Table: ' + str(t), file=sys.stderr)
            #req = borneo.TableRequest().set_statement('DROP TABLE user_eva')
            #res = store_handle.do_table_request(req, 20000, 1000)
            #print('Drop result: ' + str(res), file=sys.stderr)
    except (Exception, ValueError) as ex:
        err=json.dumps({"message": "exc {0}".format(str(ex))})
    return response.Response(
        ctx, response_data=err,
        headers={"Content-Type": "application/json"}
    )

