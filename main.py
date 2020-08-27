from klib import App


def main():
    app = App("manifests/bookinfo.yaml")
    network = App("manifests/bookinfo-gateway.yaml")

    app.k_apply()
    network.k_apply()

    # app.k_check_status()

    # uncomment to delete resources
    # app.k_delete()
    # network.k_delete()


if __name__ == '__main__':
    main()
