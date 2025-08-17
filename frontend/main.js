const apiUrl = "http://localhost:3000/major-groups";

const data = await axios.get(apiUrl).then((response) => {
  const s = JSON.stringify(response.data);
  return JSON.parse(s);
});

console.log(data);

const tabularData = [
  { id: "plants", parentId: "" },
  ...data.major_groups.map((d) => ({
    id: d,
    parentId: "plants",
  })),
];

//create a basic chart with d3.j
d3.select("graph-container").append("h1").text("Hello, D3.js!");

const margin = { top: 20, right: 20, bottom: 20, left: 20 };

const width = 800;
const height = 800;
const widthMargin = width - margin.left - margin.right;
const heightMargin = height - margin.top - margin.bottom;

const dimensions = {
  width: width,
  height: height,
  widthMargin: widthMargin,
  heightMargin: heightMargin,
};

//accessors
function sep(a, b) {
  return a.parent == b.parent ? 1 : 2;
}

const container = d3
  .select("#graph-container")
  .append("svg")
  .attr("width", dimensions.width)
  .attr("height", dimensions.height)
  .append("g")

  .attr("transform", `translate(${width / 2},${height / 2})`);

const root = d3
  .stratify()
  .id((d) => d.id)
  .parentId((d) => d.parentId)(tabularData);

const radius = width / 2 - 200;
const treeLayout = d3
  .tree()
  .size([2 * Math.PI, radius])
  .separation(sep);

treeLayout(root);

//draw links
container
  .selectAll("path.link")
  .data(root.links())
  .enter()
  .append("path")
  .attr("fill", "none")
  .attr("class", "link")
  .attr("stroke", "#555")
  .attr(
    "d",
    d3
      .linkRadial()
      .angle((d) => d.x)
      .radius((d) => d.y),
  );

//draw nodes
container
  .selectAll("circle")
  .data(root.descendants())
  .enter()
  .append("circle")
  .attr(
    "transform",
    (d) => `
    rotate(${(d.x * 180) / Math.PI - 90})
    translate(${d.y},0)
  `,
  )
  .attr("r", 5)
  .attr("fill", "black");

//draw node labels
container
  .selectAll("text")
  .data(root.descendants())
  .enter()
  .append("text")
  .attr(
    "transform",
    (d) => `rotate(${(d.x * 180) / Math.PI - 90})
translate(${d.y}, 0)
rotate(${d.x >= Math.PI ? 180 : 0})`,
  )
  .text((d) => d.data.id)
  .attr("dy", "0.31em")
  .attr("x", (d) => (d.x < Math.PI === !d.children ? 6 : -6))
  .attr("text-anchor", (d) => (d.x < Math.PI === !d.children ? "start" : "end"))
  .attr((d) => d.id);
