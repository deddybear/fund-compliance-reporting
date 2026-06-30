from pathlib import Path

from app.bootstrap import Bootstrap


def main() -> None:

    bootstrap = Bootstrap(args="")

    try:

        bootstrap.graph_loader.load(Path("configs/firm_a.yaml"))

        metric = "aggregate_non_ig_exposure"

        #
        # Query Neo4j
        #
        graph = bootstrap.graph_query_service.get_graph_path(
            metric,
        )

        if graph is None:
            print(f"[ERROR] Metric '{metric}' not found.")
            return

        print("[OK] Graph queried.")

        #
        # Convert to GraphRenderData
        #
        render_data = bootstrap.graph_builder.build(
            title=metric,
            graph=graph,
        )

        print(
            f"[OK] Nodes={len(render_data.nodes)} "
            f"Edges={len(render_data.edges)}"
        )

        #
        # Render PNG
        #
        output = Path(
            "storage/graphs/test.png"
        )

        bootstrap.graph_renderer.render(
            render_data,
            output,
        )

        print(f"[OK] PNG written to {output}")

    finally:

        bootstrap.shutdown()


if __name__ == "__main__":
    main()