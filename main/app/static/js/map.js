/* index.js */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { NavermapsProvider } from 'react-naver-maps';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <NavermapsProvider ncpClientId="r70grgn453">
    <App />
  </NavermapsProvider>
);


/* App.jsx */
import React, { useState, useEffect } from 'react';
import {
  useNavermaps,
  NaverMap,
  Marker,
  Polyline,
  InfoWindow,
} from 'react-naver-maps';

function App() {
  // ① 네이버맵 로딩 훅
  const { loaded, error, naver } = useNavermaps();

  const [buildings, setBuildings] = useState([]);
  const [start, setStart]       = useState('');
  const [end, setEnd]           = useState('');
  const [steps, setSteps]       = useState([]);
  const [highlight, setHighlight] = useState(null);
  const [info, setInfo]         = useState(null);
  const [polyPath, setPolyPath] = useState([]);

  // ② 건물 목록 불러오기
  useEffect(() => {
    fetch('/map/buildings')
      .then(res => res.json())
      .then(data => {
        setBuildings(data);
        if (data.length >= 2) {
          setStart(data[0].id);
          setEnd(data[1].id);
        }
      });
  }, []);

  // ③ 건물 선택
  const handleSelect = id => {
    fetch(`/map/select/${id}`)
      .then(res => res.json())
      .then(data => {
        const pos = { lat: data.lat, lng: data.lng };
        setHighlight(pos);
        setInfo({ name: data.name, description: data.description, pos });
      });
  };

  // ④ 길찾기
  const findPath = () => {
    if (start === end) {
      alert('출발지와 도착지를 다르게 선택하세요');
      return;
    }
    fetch(`/map/path/${start}/${end}`)
      .then(res => res.json())
      .then(data => {
        setSteps(data.steps);
        const s = buildings.find(b => b.id === start);
        const e = buildings.find(b => b.id === end);
        setPolyPath([
          { lat: s.lat, lng: s.lng },
          { lat: e.lat, lng: e.lng }
        ]);
      });
  };

  // ⑤ 로딩 및 에러 처리
  if (error)   return <p>지도 로드 실패</p>;
  if (!loaded) return <p>지도 로딩 중...</p>;

  return (
    <div>
      <h1>MAP - 한경국립대학교</h1>
      <div>
        <label>출발지: </label>
        <select value={start} onChange={e => setStart(e.target.value)}>
          {buildings.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
        </select>

        <label>도착지: </label>
        <select value={end} onChange={e => setEnd(e.target.value)}>
          {buildings.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
        </select>

        <button onClick={findPath}>길찾기</button>
      </div>

      {/* ⑥ 지도 */}
      <div style={{ width: '100%', height: '300px' }}>
        <NaverMap
          map={naver.maps.Map}
          defaultCenter={{ lat: 37.0157, lng: 127.2701 }}
          defaultZoom={16}
          style={{ width: '100%', height: '100%' }}
        >
          {highlight && (
            <Marker
              position={highlight}
              icon={{
                url: 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
                size: { width: 24, height: 35 }
              }}
            />
          )}

          {info && (
            <InfoWindow
              position={info.pos}
              content={`<div style="padding:10px;min-width:200px;"><h4>${info.name}</h4><p>${info.description}</p></div>`}
              onCloseClick={() => setInfo(null)}
            />
          )}

          {polyPath.length === 2 && (
            <Polyline
              path={polyPath}
              strokeColor="#FF0000"
              strokeOpacity={0.7}
              strokeWeight={5}
            />
          )}
        </NaverMap>
      </div>

      {/* ⑦ 단계별 안내 */}
      <div>
        {steps.map((step, idx) => (
          <div key={idx}>{step.instruction} ({step.distance})</div>
        ))}
      </div>

      {/* ⑧ 사이드바: 건물 클릭 리스트 */}
      <div>
        {buildings.map(b => (
          <div
            key={b.id}
            style={{ cursor: 'pointer', padding: '4px 0' }}
            onClick={() => handleSelect(b.id)}
          >
            {b.name}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

