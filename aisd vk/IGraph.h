#pragma once

struct IGraph {
    virtual ~IGraph() {}
    virtual void AddEdge(int from, int to) = 0;
    virtual int VerticesCount() const = 0;
    virtual int* GetNextVertices(int vertex, int& count) const = 0;
    virtual int* GetPrevVertices(int vertex, int& count) const = 0;
};