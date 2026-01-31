import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [tickets, setTickets] = useState([])
  const [selectedTicket, setSelectedTicket] = useState(null)

  // Poll backend
  useEffect(() => {
    const interval = setInterval(fetchState, 2000)
    fetchState()
    return () => clearInterval(interval)
  }, [])

  const fetchState = async () => {
    try {
      const res = await fetch('http://localhost:8000/agent/state')
      const data = await res.json()
      setTickets(data.tickets.reverse()) // Newest first

      // Update selected ticket if it exists
      if (selectedTicket) {
        const updated = data.tickets.find(t => t.id === selectedTicket.id)
        if (updated) setSelectedTicket(updated)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const approveAction = async (ticketId) => {
    await fetch(`http://localhost:8000/agent/approve?ticket_id=${ticketId}`, { method: 'POST' })
    fetchState()
  }

  const startSimulation = async (scenario) => {
    await fetch(`http://localhost:8000/simulation/start?scenario_id=${scenario}`, { method: 'POST' })
    fetchState()
  }

  return (
    <div className="dashboard">
      <div className="sidebar">
        <h2>Active Tickets</h2>
        <div className="controls">
          <button onClick={() => startSimulation("checkout_failure")}>Sim: Checkout Fail</button>
          <button onClick={() => startSimulation("webhook_failure")}>Sim: Webhook Fail</button>
        </div>
        <div className="ticket-list">
          {tickets.map(ticket => (
            <div
              key={ticket.id}
              className={`ticket-card ${selectedTicket?.id === ticket.id ? 'active' : ''}`}
              onClick={() => setSelectedTicket(ticket)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>#{ticket.id}</strong>
                <span className={`status-badge status-${ticket.status}`}>{ticket.status}</span>
              </div>
              <div style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>
                {ticket.signal?.scenario_name}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="main-content">
        {selectedTicket ? (
          <>
            <div className="header">
              <h2>Ticket #{selectedTicket.id}: {selectedTicket.signal?.scenario_name}</h2>
              <p>{selectedTicket.signal?.description}</p>
            </div>

            <div className="timeline">
              <h3>Agent Timeline</h3>
              {selectedTicket.steps.map((step, idx) => (
                <div key={idx} className="timeline-step">
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>{step.timestamp.split('T')[1].split('.')[0]}</div>
                  <strong>{step.stage}</strong>: {step.message}
                  {step.output && (
                    <pre>{JSON.stringify(step.output, null, 2)}</pre>
                  )}
                </div>
              ))}
            </div>

            {selectedTicket.status === 'pending_approval' && (
              <div className="actions" style={{ marginTop: '2rem', padding: '1rem', background: '#30363d' }}>
                <h3>Requires Approval</h3>
                <p>The agent wants to execute a HIGH RISK action.</p>
                <button onClick={() => approveAction(selectedTicket.id)}>APPROVE ACTION</button>
              </div>
            )}
          </>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            Select a ticket to view details
          </div>
        )}
      </div>
    </div>
  )
}

export default App
