#pragma once
#include "IGraph.h"

class MatrixGraph : public IGraph {
public:
    explicit MatrixGraph(int verticesCount);
    explicit MatrixGraph(const IGraph& graph);
    ~MatrixGraph();
    
    void AddEdge(int from, int to) override;
    int VerticesCount() const override;
    int* GetNextVertices(int vertex, int& count) const override;
    int* GetPrevVertices(int vertex, int& count) const override;

private:
    int verticesCount;
    bool** matrix;
};