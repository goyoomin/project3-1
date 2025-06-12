const width = 800;
const height = 600;

const projection = d3.geoMercator()
    .scale(1) // 초기 스케일
    .translate([0, 0]); // 초기 중심

const path = d3.geoPath().projection(projection);

// Proj4 좌표계 정의
proj4.defs(
    "EPSG:5179",
    "+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=200000 +y_0=500000 +ellps=GRS80 +units=m +no_defs"
);

const proj5179ToWGS84 = proj4("EPSG:5179", "WGS84");

console.log("korea_map.js loaded!");

document.addEventListener("DOMContentLoaded", function () {
    const svg = d3.select("#map-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    d3.json("/static/js/korea_map.json").then((topoData) => {
        if (!topoData || !topoData.objects.korea_map) {
            throw new Error("Invalid TopoJSON structure.");
        }

        const geoData = topojson.feature(topoData, topoData.objects.korea_map);
        console.log("GeoJSON Data Before Transformation:", geoData);

        // 좌표 변환 및 유효하지 않은 좌표 필터링
        geoData.features.forEach(feature => {
            if (feature.geometry.type === "Polygon") {
                feature.geometry.coordinates = feature.geometry.coordinates.map(polygon =>
                    polygon.map(coords => {
                        if (coords.length === 2) {
                            const [x, y] = proj5179ToWGS84.forward(coords);
                            return isFinite(x) && isFinite(y) ? [x, y] : null;
                        }
                        return null;
                    }).filter(coords => coords !== null)
                );
            } else if (feature.geometry.type === "MultiPolygon") {
                feature.geometry.coordinates = feature.geometry.coordinates.map(multiPolygon =>
                    multiPolygon.map(polygon =>
                        polygon.map(coords => {
                            if (coords.length === 2) {
                                const [x, y] = proj5179ToWGS84.forward(coords);
                                return isFinite(x) && isFinite(y) ? [x, y] : null;
                            }
                            return null;
                        }).filter(coords => coords !== null)
                    )
                );
            }
        });

        console.log("GeoJSON Data After Transformation:", geoData);

        // 투영을 GeoJSON 데이터에 맞추기
        const bounds = path.bounds(geoData);
        const dx = bounds[1][0] - bounds[0][0];
        const dy = bounds[1][1] - bounds[0][1];
        const scale = Math.min(width / dx, height / dy) * 0.9;
        const translate = [
            width / 2 - scale * (bounds[0][0] + bounds[1][0]) / 2,
            height / 2 - scale * (bounds[0][1] + bounds[1][1]) / 2,
        ];
        projection.scale(scale).translate(translate);

        console.log("Projection Scale and Translate:", scale, translate);

        // SVG에 경로 추가
        svg.selectAll("path")
            .data(geoData.features)
            .enter()
            .append("path")
            .attr("d", path)
            .attr("stroke", "#ffffff")
            .attr("stroke-width", 1)
            .attr("fill", "#69b3a2")
            .on("click", function (event, d) {
                const selectedRegion = d.properties.CTP_KOR_NM;
        
                // 1번 드롭다운 메뉴 업데이트
                const dropdown = document.getElementById("region-dropdown");
                dropdown.value = selectedRegion;
        
                // 2번 드롭다운 자동 업데이트
                updateCities();
            })
            .on("mouseover", function () {
                d3.select(this).attr("fill", "#f39c12");
            })
            .on("mouseout", function () {
                d3.select(this).attr("fill", "#69b3a2");
            });

            function translateTolabel(d) {
                let arr = path.centroid(d);
                if (d.properties.CTP_KOR_NM === "경기도") {
                    // 경기도 글씨 살짝 내리기
                    arr[1] += 25; // y축 아래로 이동
                } else if (d.properties.CTP_KOR_NM === "충청남도") {
                    // 충청남도 글씨 살짝 더 내리기
                    arr[1] += 20; // y축 아래로 이동
                } else if (d.properties.CTP_KOR_NM === "대전광역시") {
                    arr[1] += 10; // y축 아래로 이동
                } else if (d.properties.CTP_KOR_NM === "충청북도") {
                    arr[1] -= 10; // y축 아래로 이동
                } 
                return arr;
            }
            
            // 텍스트 추가 코드 (위치 조절 포함)
            svg.selectAll("text")
            .data(geoData.features)
            .enter()
            .append("text")
            .attr("x", d => translateTolabel(d)[0])
            .attr("y", d => translateTolabel(d)[1])
            .attr("text-anchor", "middle")
            .style("font-size", "14px")
            .style("font-weight", "bold")
            
            .text(d => d.properties.CTP_KOR_NM);
        console.log("Paths added:", geoData.features.length);
    }).catch((error) => {
        console.error("Error loading or processing the map data:", error);
    });

    
});
