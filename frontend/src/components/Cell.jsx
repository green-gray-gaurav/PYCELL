import React, { useState } from 'react'

function makeVersion(content) {
  return { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), content, ts: Date.now() }
}

export default function Cell({ cell, onDelete, onChange, index }) {
  const [content, setContent] = useState(cell.content || '')

  function applyChange(newContent) {
    setContent(newContent)
    const updated = { ...cell, content: newContent }
    onChange(updated)
  }

  function createVersion() {
    const v = makeVersion(content)
    const updated = { ...cell, versions: [...(cell.versions || []), v], currentVersion: (cell.versions || []).length }
    onChange(updated)
  }

  function deleteVersion(versionId) {
    const versions = (cell.versions || []).filter((v) => v.id !== versionId)
    const updated = { ...cell, versions, currentVersion: versions.length - 1 }
    onChange(updated)
  }

  function selectVersion(versionId) {
    const v = (cell.versions || []).find((x) => x.id === versionId)
    if (!v) return
    const updated = { ...cell, content: v.content }
    onChange(updated)
    setContent(v.content)
  }

  return (
    <div className="cell">
      <div className="cell-header">
        <strong>Cell {index}</strong>
        <div className="cell-actions">
          <select onChange={(e) => selectVersion(e.target.value)} value={cell.versions && cell.versions[cell.currentVersion] ? cell.versions[cell.currentVersion].id : ''}>
            <option value="">Current</option>
            {(cell.versions || []).map((v) => (
              <option key={v.id} value={v.id}>{new Date(v.ts).toLocaleString()}</option>
            ))}
          </select>
          <button onClick={createVersion}>New Version</button>
          {/* <button onClick={() => { const vid = cell.versions && cell.versions[cell.currentVersion] ? cell.versions[cell.currentVersion].id : null; if (vid) deleteVersion(vid) else alert('No version selected') }}>Delete Version</button> */}
          <button className="delete" onClick={onDelete}>Delete Cell</button>
        </div>
      </div>
      <textarea value={content} onChange={(e) => applyChange(e.target.value)} />
    </div>
  )
}
