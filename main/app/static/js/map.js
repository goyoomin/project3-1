import React, { useState, useEffect } from 'react';
import {
  useNavermaps,
  NaverMap,
  Marker,
  Polyline,
  InfoWindow,
} from 'react-naver-maps';

function App() {
  const { loaded, error, naver } = useNavermaps();

  const [buildings, setBuildings] = useState([]);
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [highlight, setHighlight] = useState(null);
  const [info, setInfo] = useState(null);
  const [polyPath, setPolyPath] = useState([]);

  // 건물 목록 불러오기
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

  // 건물 클릭 시 InfoWindow 표시
  const handleSelect = id => {
    const b = buildings.find(b => b.id === id);
    if (b) {
      const pos = { lat: b.lat, lng: b.lng };
      setHighlight(pos);
      setInfo({ name: b.name, description: b.description, pos });
    }
  };

  // 길찾기(직선) 버튼
  const findPath = () => {
    if (start === null || end === null) {
      alert('출발지와 도착지를 선택하세요!');
      return;
    }
    if (start === end) {
      alert('출발지와 도착지는 달라야 합니다.');
      return;
    }
    const s = buildings.find(b => b.id === start);
    const e = buildings.find(b => b.id === end);
    if (!s || !e) {
      alert('건물 정보를 찾을 수 없습니다.');
      setPolyPath([]);
      return;
    }
    setPolyPath([
      { lat: s.lat, lng: s.lng },
      { lat: e.lat, lng: e.lng }
    ]);
  };

  if (error) return <p>지도 로드 실패</p>;
  if (!loaded) return <p>지도 로딩 중...</p>;

  // 버튼 비활성화 조건
  const canFindPath = buildings.length > 1 && start !== null && end !== null;

  return (
    <div>
      <h1>MAP - 한경국립대학교</h1>
      {/* 출발지/도착지 select UI */}
      <div>
        <label>출발지: </label>
        <select value={start ?? ''} onChange={e => setStart(Number(e.target.value))}>
          {buildings.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
        </select>

        <label>도착지: </label>
        <select value={end ?? ''} onChange={e => setEnd(Number(e.target.value))}>
          {buildings.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
        </select>

        <button type="button" onClick={findPath} disabled={!canFindPath}>길찾기</button>
      </div>

      {/* 지도 */}
      <div style={{ width: '100%', height: '300px' }}>
        <NaverMap
          map={naver.maps.Map}
          defaultCenter={{ lat: 37.0157, lng: 127.2701 }}
          defaultZoom={16}
          style={{ width: '100%', height: '100%' }}
        >
          {/* 건물마다 마커 표시 */}
          {buildings.map(b => (
            <Marker
              key={b.id}
              position={{ lat: b.lat, lng: b.lng }}
              onClick={() => handleSelect(b.id)}
            />
          ))}

          {/* 건물 강조 마커 */}
          {highlight && (
            <Marker
              position={highlight}
              icon={{
                url: 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
                size: { width: 24, height: 35 }
              }}
            />
          )}

          {/* 설명창 (InfoWindow) - 출발지/도착지 버튼 */}
          {info && (
            <InfoWindow
              position={info.pos}
              onCloseClick={() => setInfo(null)}
            >
              <div style={{ padding: 10, minWidth: 200 }}>
                <h4>{info.name}</h4>
                <p>{info.description}</p>
                <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
                  <button
                    style={{ background: '#3d8bfd', color: 'white', border: 0, borderRadius: 4, padding: '4px 8px' }}
                    onClick={() => {
                      setStart(buildings.find(b => b.name === info.name)?.id);
                      setInfo(null);
                    }}
                  >
                    출발지
                  </button>
                  <button
                    style={{ background: '#fa5252', color: 'white', border: 0, borderRadius: 4, padding: '4px 8px' }}
                    onClick={() => {
                      setEnd(buildings.find(b => b.name === info.name)?.id);
                      setInfo(null);
                    }}
                  >
                    도착지
                  </button>
                </div>
              </div>
            </InfoWindow>
          )}

          {/* Polyline: 출발~도착 직선 */}
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

      {/* 사이드바: 건물 목록 */}
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
