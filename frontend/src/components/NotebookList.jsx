import React, { useState } from 'react'

export default function NotebookList({ notebooks, current, onCreate, onDelete, onRename, onLoad }) {
  const [newName, setNewName] = useState('')

  return (
    <aside className="notebook-list">
      <div className="list-header">
        <h2>Notebooks</h2>
        <div className="new-row">
        
          <input placeholder="New notebook name" value={newName} onChange={(e) => setNewName(e.target.value)} />
          <button onClick={() => { onCreate(newName); setNewName('') }}>Create</button>
       
        </div>
      </div>
      <ul>
        {(notebooks).length === 0 && <li className="empty">No notebooks</li>}
        {(notebooks).map((name) => (
          <li key={name} className={name === current ? 'active' : ''}>
            <button className="load" onClick={() => onLoad(name)}>{name}</button>
            
            
            <button className="rename" onClick={() => {
              const nn = prompt('New name', name)


              if (nn) onRename(name, nn)


            }}>Rename</button>
            
            
            <button className="delete" onClick={() => onDelete(name)}>Delete</button>
          
          
          </li>
        ))}
      </ul>
    </aside>
  )
}
