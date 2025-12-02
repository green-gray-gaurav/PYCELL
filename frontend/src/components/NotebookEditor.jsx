import React, { useEffect, useState } from 'react'
import Cell from './Cell'
import * as api from '../api'

export default function NotebookEditor({ notebook, onSave, onUpdate, onDelete }) {
  const [notebookData, setNotebookData] = React.useState(new Map())
  

  useEffect(() => {
    console.log('notebook changed', notebook)
    getCellData()
  }, [notebook])
  

  function getCellData() {

    fetch('http://127.0.0.1:5000/get_cell_data', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
      
    })
      .then((res) => res.json())
      .then((data) => {
        
        console.log(data)
        let new_data = new Map()
        Object.keys(data.cell_data).forEach((line_index) => {
          new_data.set(line_index, new Map())
          Object.keys(data.cell_data[line_index]).forEach((index) => {
            new_data.get(line_index).set(index, data.cell_data[line_index][index])

          })
        })
        setNotebookData(new_data)
        console.log(notebookData)
      })
      .catch((err) => {
        alert('sdfdsf')
        console.log('create_notebook error', err)
      })

  }
  function addCell() {
    fetch('http://127.0.0.1:5000/add_cell', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },

      body: JSON.stringify({  line_index :  notebookData.size , index : 
        (notebookData.has(notebookData.size) ? notebookData.get(notebookData.size).size : 0) 
      })
      
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        
      })
      .catch((err) => {
        alert('sdfdsf')
        console.log('create_notebook error', err)
      })

  }

  function deleteCell(line_index, index) {
      fetch('http://127.0.0.1:5000/delete_cell', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },

      body: JSON.stringify({  line_index :  line_index , index : index }  ) 
      
      
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        
      })
      .catch((err) => {
        alert('sdfdsf')
        console.log('create_notebook error', err)
      })
    
  }

  function updateCell(updated) {

    
  }

  return (
    <div className="editor">

      <div className="editor-header">

        <h2>{notebook}</h2>

        <div className="editor-actions">
          <button onClick={getCellData}>Load Cells</button>
          <button onClick={() => onSave(notebook)}>Save (download + local)</button>
          <button onClick={() => { if (confirm('Delete notebook?')) onDelete() }}>Delete Notebook</button>
        
        </div>

      </div>

      <div className="cells">
        {[...notebookData.keys()].map((line_index) => (
          [...notebookData.get(line_index).keys()].map((index) => (
            <Cell 
              key={`${line_index}-${index}`}
              cell={notebookData.get(line_index).get(index)} 
              index={`${line_index}-${index}`}
              onDelete={() => deleteCell(line_index, index)}
            />
          ))
        ))}
        <div className="add-cell-row">

          <button onClick={addCell}>+ Add Cell</button>
        </div>
      </div>
    </div>
  )
}
