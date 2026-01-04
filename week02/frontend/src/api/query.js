import client from './client';

export const executeSql = (connectionId, sql) => client.post('/query/sql', { connection_id: connectionId, sql });
export const executeNlQuery = (connectionId, question) => client.post('/query/natural-language', { connection_id: connectionId, question });
