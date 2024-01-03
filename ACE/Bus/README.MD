# BusConfig Class

This class provides methods to interact with the `South_bound_bus`, `north_bound_bus`, and `conversation` tables in the SQLite database.

## Methods

### South_bound_bus Table

- `create_south_bound_bus(layer, message, system_prompt)`: Inserts a new record into the `South_bound_bus` table.
- `read_south_bound_bus(id)`: Retrieves a record with the specified `id` from the `South_bound_bus` table.
- `update_south_bound_bus(id, layer, message, system_prompt)`: Updates the record with the specified `id` in the `South_bound_bus` table.
- `delete_south_bound_bus(id)`: Deletes the record with the specified `id` from the `South_bound_bus` table.
- `get_all_south_bound_bus(limit)`: Retrieves the first `limit` number of records from the `South_bound_bus` table.

### North_bound_bus Table

- `create_north_bound_bus(layer, message, system_prompt)`: Inserts a new record into the `north_bound_bus` table.
- `read_north_bound_bus(id)`: Retrieves a record with the specified `id` from the `north_bound_bus` table.
- `update_north_bound_bus(id, layer, message, system_prompt)`: Updates the record with the specified `id` in the `north_bound_bus` table.
- `delete_north_bound_bus(id)`: Deletes the record with the specified `id` from the `north_bound_bus` table.
- `get_all_north_bound_bus(limit)`: Retrieves the first `limit` number of records from the `north_bound_bus` table.

### Conversation Table

- `create_conversation(role, content)`: Inserts a new record into the `conversation` table.
- `read_conversation(id)`: Retrieves a record with the specified `id` from the `conversation` table.
- `update_conversation(id, role, content)`: Updates the record with the specified `id` in the `conversation` table.
- `delete_conversation(id)`: Deletes the record with the specified `id` from the `conversation` table.
- `get_all_conversations(limit)`: Retrieves the first `limit` number of records from the `conversation` table.