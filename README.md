# AWS Lambda + Dynamodb + Serverless Stack Template

```
git clone git@github.com:zihaolam/aws-lambda-template.git
```

## What's in the stack

-   [AWS deployment](https://aws.com) with [Serverless Framework](https://www.serverless.com/)
-   [DynamoDB Database](https://aws.amazon.com/dynamodb/)
-   [AWS Cognito](https://aws.amazon.com/cognito/)
-   DynamoDB access via [`pynamodb`](https://github.com/pynamodb/PynamoDB)
-   Unit Testing with [pytest](https://docs.pytest.org/en/7.2.x/)
-   Code formatting with [black](https://pypi.org/project/black/#:~:text=Black%20is%20the%20uncompromising%20Python,energy%20for%20more%20important%20matters.)
-   Automated Documentation with [swagger](https://swagger.io/)

## Development

-   Clone Repo:

    ```sh
    git clone git@github.com:zihaolam/aws-lambda-template.git
    ```

-   Install dependencies:

    ```sh
    yarn install
    pipenv install
    ```

-   Start local dynamodb instance (Make sure docker is running):

    ```sh
    yarn db:dev
    ```

-   Create single table with indexes:

    ```sh
    yarn db:create:local
    ```

-   Start serverless-offline local server for AWS Lambda:

    ```sh
    yarn dev
    ```

This starts your app in development mode, rebuilding assets on file changes.
