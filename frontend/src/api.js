const API_BASE = (typeof process !== 'undefined' && process.env.REACT_APP_API_BASE) || '/api'

async function request(path, opts = {}) {
  const url = `${API_BASE}${path}`
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    ...opts,
  })
  if (!res.ok) {
    const text = await res.text()
    const err = new Error(`API ${res.status} ${res.statusText}: ${text}`)
    err.status = res.status
    throw err
  }
  try {
    return await res.json()
  } catch (e) {
    return null
  }
}

export async function listNotebooks() {
  return await request('/notebooks')
}

export async function createNotebookAPI(name) {
  return await request('/notebooks', { method: 'POST', body: JSON.stringify({ name }) })
}

export async function deleteNotebookAPI(name) {
  return await request(`/notebooks/${encodeURIComponent(name)}`, { method: 'DELETE' })
}

export async function renameNotebookAPI(oldName, newName) {
  return await request(`/notebooks/${encodeURIComponent(oldName)}/rename`, { method: 'POST', body: JSON.stringify({ newName }) })
}

export async function loadNotebookAPI(name) {
  return await request(`/notebooks/${encodeURIComponent(name)}`)
}

export async function saveNotebookAPI(name, notebook) {
  return await request(`/notebooks/${encodeURIComponent(name)}`, { method: 'POST', body: JSON.stringify({ notebook }) })
}

export async function addCellAPI(name) {
  return await request(`/notebooks/${encodeURIComponent(name)}/cells`, { method: 'POST', body: JSON.stringify({}) })
}

export async function deleteCellAPI(name, cellId) {
  return await request(`/notebooks/${encodeURIComponent(name)}/cells/${encodeURIComponent(cellId)}`, { method: 'DELETE' })
}

export async function updateCellAPI(name, cell) {
  return await request(`/notebooks/${encodeURIComponent(name)}/cells/${encodeURIComponent(cell.id)}`, { method: 'PUT', body: JSON.stringify({ cell }) })
}

export async function createCellVersionAPI(name, cellId, content) {
  return await request(`/notebooks/${encodeURIComponent(name)}/cells/${encodeURIComponent(cellId)}/versions`, { method: 'POST', body: JSON.stringify({ content }) })
}

export async function deleteCellVersionAPI(name, cellId, versionId) {
  return await request(`/notebooks/${encodeURIComponent(name)}/cells/${encodeURIComponent(cellId)}/versions/${encodeURIComponent(versionId)}`, { method: 'DELETE' })
}

export default {
  listNotebooks,
  createNotebookAPI,
  deleteNotebookAPI,
  renameNotebookAPI,
  loadNotebookAPI,
  saveNotebookAPI,
  addCellAPI,
  deleteCellAPI,
  updateCellAPI,
  createCellVersionAPI,
  deleteCellVersionAPI,
}
