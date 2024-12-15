import React, { useState, useCallback } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

const App = () => {
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [path, setPath] = useState([]);

  const MapClickHandler = useCallback(() => {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng;
        if (!origin) {
          setOrigin([lat, lng]);
        } else if (!destination) {
          setDestination([lat, lng]);
        }
      },
    });
    return null;
  }, [origin, destination]);

  const calculateShortestPath = async () => {
    if (!origin || !destination) {
      alert("Please select both origin and destination points.");
      return;
    }
    try {
      const response = await axios.post("http://localhost:5000/shortest-path", {
        origin,
        destination,
      });
      setPath(response.data.path);
    } catch (error) {
      const errorMessage =
        error.response?.data?.error || error.message || "Unable to calculate shortest path.";
      alert(`Error: ${errorMessage}`);
    }
  };

  const resetSelection = () => {
    setOrigin(null);
    setDestination(null);
    setPath([]);
  };

  return (
    <div className="container my-5">
      <h1 className="text-center mb-4" style={{ color: "black" }}>Bengaluru Shortest Path Finder</h1>
      <div className="row">
        {/* Left Column: Info & Buttons */}
        <div className="col-12 col-md-6 mb-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title" style={{ color: "red" }}>Select Origin and Destination</h5>
              <p className="card-text">Click on the map to select origin and destination:</p>
              <p>
                <strong style={{ color: "blue" }}>Origin:</strong> {origin ? `${origin[0]}, ${origin[1]}` : "Not selected"}
              </p>
              <p>
                <strong style={{ color: "blue" }}>Destination:</strong> {destination ? `${destination[0]}, ${destination[1]}` : "Not selected"}
              </p>
              <div className="d-grid gap-2">
                <button className="btn btn-primary" onClick={calculateShortestPath}>
                  Find Shortest Path
                </button>
                <button className="btn btn-secondary" onClick={resetSelection}>
                  Reset
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Map */}
        <div className="col-12 col-md-6">
          <div className="card shadow-sm">
            <div className="card-body p-0">
              <MapContainer
                center={[12.9716, 77.5946]}
                zoom={12}
                style={{ height: "400px", width: "100%" }}
              >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                {origin && <Marker position={origin} />}
                {destination && <Marker position={destination} />}
                {path.length > 1 && <Polyline positions={path} color="blue" />}
                <MapClickHandler />
              </MapContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
