#pragma once
#include "IGraph.h"

struct Edge {
    int from;
    int to;
    Edge* next;
    Edge(int f, int t) : from(f), to(t), next(nullptr) {}
};

class ArcGraph : public IGraph {
public:
    explicit ArcGraph(int verticesCount);
    explicit ArcGraph(const IGraph& graph);
    ~ArcGraph();
    
    void AddEdge(int from, int to) override;
    int VerticesCount() const override;
    int* GetNextVertices(int vertex, int& count) const override;
    int* GetPrevVertices(int vertex, int& count) const override;

private:
    int verticesCount;
    Edge* edges;
};