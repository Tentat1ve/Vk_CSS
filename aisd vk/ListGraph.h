#pragma once
#include "IGraph.h"

class ListGraph : public IGraph {
public:
    explicit ListGraph(int verticesCount);
    explicit ListGraph(const IGraph& graph);
    ~ListGraph();
    
    void AddEdge(int from, int to) override;
    int VerticesCount() const override;
    int* GetNextVertices(int vertex, int& count) const override;
    int* GetPrevVertices(int vertex, int& count) const override;

private:
    int verticesCount;
    int** adjacencyLists;
    int* listSizes;
};